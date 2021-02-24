pragma specify 0.1

methods {
	init_state()
	points(address) returns uint256 envfree
	vote(address,address,address)
 	voted(address) returns bool envfree
	winner() returns address envfree
}

definition MAXINT() returns uint256 =
	0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

/*
After voting, a user is marked as voted
    vote(e, f, s, t) => voted(e.msg.sender)
*/
rule integerityVote(address f, address s, address t) {
	env e;
	vote(e, f, s, t);
	assert voted(e.msg.sender), "A user voted without being marked accordingly";
}

/*
Single vote per user
	A user can not vote if he has voted before
 	voted(e.msg.sender) => ㄱvote(e, f, s, t)
*/
rule singleVote(address f, address s, address t) {
	env e;
	bool has_voted_before = voted(e.msg.sender);
	vote@withrevert(e, f, s, t);
	assert has_voted_before => lastReverted, "Double voting is not allowed";
}

/*
Integrity of points:
	When voting, the points each candidate gets are updated as expected. 
	This rule also verifies that there are three distinct candidates.

	{ points(f) = f_points ⋀ points(s) = s_points ⋀ points(t) = t_points }
	vote(e, f, s, t)
	{ points(f) = f_points + 3 ⋀ points(s) = s_points + 2 ⋀ points(t) = t_points + 1 }
*/
rule integrityPoints(address f, address s, address t) {
	env e;
	uint256 f_points = points(f);
	uint256 s_points = points(s);
	uint256 t_points = points(t);
	vote(e, f, s, t);
	assert points(f) == f_points + 3 &&
		   points(s) == s_points + 2 &&
		   points(t) == t_points + 1,   "unexpected change of points";
}

/*
Integrity of voted:
	Once a user cast her vote, she is marked as voted globally (for all future states)
	vote(e, f, s, t)  Globally voted(e.msg.sender)
*/
rule golballyVoted(address x, method f) {
	require voted(x);
	env eF;
	calldataarg arg;
	f(eF,arg);
	assert voted(x), "Once a user voted, he is marked as voted in all future states";
}

/*
 Integrity of winner
	The winner has the most points.
	winner() = w ∀address c. points(c) ≤ points(w)
*/
invariant integrityPointsOfWinner(address c)
			points(winner()) >= points(c)

/*
Vote is the only state-changing function. 
A vote can only affect the voter and the selected candidates, and has no effect on other addresses.
	∀address c, c ≠ {f, s, t}.
	{ c_points = points(c) ⋀ b = voted(c) }  vote(x, f, s, t)  { points(c) = c_points ⋀ ( voted(c) = b V c = x ) }
*/
rule noEffect(method m) {
	address c;
	env e;
	uint256 c_points = points(c);
	bool c_voted = voted(c);
	if (m.selector == vote(address, address, address).selector) {
		address f;
		address s;
		address t;
		require( c != f  &&  c != s  &&  c != t );
		vote(e, f, s, t);
	}
	else {
		calldataarg args;
		m(e, args);
	}
	assert ( voted(c) == c_voted || c  == e.msg.sender ) &&
			 points(c) == c_points, "unexpected change to others points or voted";
}


/*
Commutativity of votes.
	The order of votes is not important
	vote(e, f, s, t) ; vote(e’, f’, s’, t’)  ～  vote(e’, f’, s’, t’) ; vote(e, f, s, t)
*/
rule voteCommutativity(address f1, address s1, address t1, address f2, address s2, address t2) {
	env e1;
	env e2;
	address c;
	address y;
	storage init = lastStorage;  // Both scenarios starts from the same initial state

	// First 1 votes, then 2
	vote(e1, f1, s1, t1);
	vote(e2, f2, s2, t2);
	uint256 c_points_P1 = points(c);
	bool y_voted_P1 = voted(y);
	uint256 winner_P1 = points(winner());

	// First 2 votes, then one
	vote(e2, f2, s2, t2) at init;
	vote(e1, f1, s1, t1);
	uint256 c_points_P2 = points(c);
	bool y_voted_P2 = voted(y);
	uint256 winner_P2 = points(winner());

	// Assert commutativity
	assert c_points_P1 == c_points_P2 &&  y_voted_P1 == y_voted_P2 && winner_P1 == winner_P2, 
		"vote() is not commutative";
}


/*
Ability to vote
	If a user can vote, no other user can prevent him to do so by any operation.
 	vote(e, f, s, t) ~ op; vote(e, f, s, t)
*/
rule allowVote(address f, address s, address t, method m) {
	env e;
	storage init = lastStorage;
	vote(e, f, s, t);  // Ensures the user can vote

	env eOther;
	require (e.msg.sender != eOther.msg.sender);
	calldataarg args;
	m(eOther, args) at init;

	require points(f) < MAXINT() - 3 && points(s) < MAXINT() - 2 && points(t) < MAXINT(); // No overflow

	vote@withrevert(e, f, s, t);

	assert !lastReverted, "a user who didn't vote yet should be able to do so unless there is an overflow";
}


/*
Participation criterion
	Abstaining from an election can not help a voter's preferred choice
	https://en.wikipedia.org/wiki/Participation_criterion


	!{ winner() != f} { !vote } { winner = f }
	!exists state s
	( !vote(e, f, s, t) on state s => winner() = f )
	and
	( vote(e, f, s, t) on state s => winner() != f )


	for every state s
	!( !vote(e, f, s, t) => winner() = f )
	or
	!( vote(e, f, s, t) && winner() != f )


*/
rule participationCriterion(address f, address s, address t) {
	env e;
	address w1 = winner();
	require points(w1) >= points(f);
	require points(w1) >= points(s);
	require points(w1) >= points(t);
	vote(e, f, s, t);
	address w2 = winner();
	assert w1 == f => w2 == f, "winner changed unexpectedly";
}

