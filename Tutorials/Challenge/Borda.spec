pragma specify 0.1
methods {
	init_state()
	points(address) returns uint256  envfree
 	voted(address) returns bool  envfree
	winner() returns address envfree
	vote(address,address,address)
}

definition MAXINT() returns uint256 =
	0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

/*
After voting, a user is marked as voted
    vote(x,f,s,t) =>  voted(x)
*/
    rule integerityVote(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		vote(e,f,s,t);
		assert voted(x), "expecting voted to be true after voting";
	}

/*
Single vote per user
	A user can not vote if he has voted before
 	voted(x) => ㄱvote(x,f,s,t)
*/
	rule singleVote(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		bool before =  voted(x);
		vote@withrevert(e,f,s,t);
		assert before => lastReverted, "expecting to deny voting for voted users";
	}

/*
Integrity of points:
	Points is updated as required, this rule also verifies that there are three distinct candidates
	{ f_points = points(f) ⋀ s_points = points(s) ⋀ t_points = points(t)}
	vote(x,f,s,t)
	{ points(f) = f_points+3 ⋀ points(s) = s_pointss+2 ⋀ t_points = points(t)+1 }
*/
	rule integrityPoints(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		uint256  f_points =  points(f);
		uint256  s_points =  points(s);
		uint256  t_points =  points(t);
		vote(e,f,s,t);
		assert points(f) == f_points +3 &&
			   points(s) == s_points +2 &&
			   points(t) == t_points +1, "unexpected change to points";
	}

/*
Integrity of voted:
	Once a user issue a vote operation he is marked as voted globally (for all next states)
	vote(x,f,s,t)  Globally voted(x)
*/
	rule golballyVoted(address x, method f) {
		require  voted(x);
		env eF;
		calldataarg arg;
		f(eF,arg);
		assert voted(x), "once voting expecting to stay voted";
	}

/*
 Integrity of winner
	The winner has the most points
	winner() = w  ∀address c. points(c) ≤  points(w)
*/
    invariant integrityPointsOfWinner(address c)
                points(winner()) >= points(c)

/*
No effect on other candidates:
	∀address c, c≠{f,s,t}.
	{c_points = points(c) ⋀ b = voted(c) }  vote(x,f,s,t) {points(c) = c_points ⋀ ( voted(c) = b  V  c = x }
*/
	rule noEffect(address x, method m) {
		address c;
		env e;
		require(x==e.msg.sender);
		uint256  c_points = points(c);
		bool c_voted = voted(c);
		if (m.selector == vote(address, address, address).selector) {
		    address f;
		    address s;
		    address t;
    	    require( c!=f &&  c!=s  && c!=t);
        	vote(e,f,s,t);
        }
    	else {
    	    calldataarg args;
    	    m(e,args);
    	}
		assert ( voted(c) == c_voted || c  == x ) &&
		        points(c) == c_points, "unexpected change to others points or voted";
	}


 /*
Commutative of votes
	Order of votes is not important
	vote(x,f,s,t)  ; vote(x’,f’,s’,t’)  ～  vote(x’,f’,s’,t’) ; vote(x,f,s,t)
*/
	rule commutative(address x1, address f1, address s1, address t1, address x2, address f2, address s2, address t2) {
		env e1;
		env e2;
		address c;
		address y;
		require(x1==e1.msg.sender);
		require(x2==e2.msg.sender);
		storage init = lastStorage;
		vote(e1,f1,s1,t1);
		vote(e2,f2,s2,t2);
		uint256  c_points_P1 =  points(c);
		bool y_voted_P1 =  voted(y);
		uint256 winner_P1 =  points(winner());
		vote(e2,f2,s2,t2) at init;
		vote(e1,f1,s1,t1);
		uint256  c_points_P2 =  points(c);
		bool y_voted_P2 =  voted(y);
		uint256 winner_P2 =  points(winner());
		assert c_points_P1 == c_points_P2 &&  y_voted_P1 == y_voted_P2 && winner_P1 == winner_P2, "vote is not commutative";
	}


/*
Able to vote
	If a user can vote he can do so after someone else operation
 	vote(x,f,s,t) ~ op;vote(x,f,s,t)
*/
	rule allowVote(address x, address o, address f, address s, address t, method m) {
		env e;
		require(x==e.msg.sender);
		storage init = lastStorage;
		vote(e,f,s,t);

		require (o!=x && o==eOther.msg.sender);
		calldataarg args;
		env eOther;
        m(eOther,args) at init;
        require points(f) < MAXINT()-3 && points(s) < MAXINT()-2 && points(t) < MAXINT();
        vote@withrevert(e,f,s,t);
		assert !lastReverted, "expecting to allow voting for nonvoted users, unless maxint reached";
	}


/*
Participation criterion
	Abstaining from an election can not help a voter's preferred choice
	https://en.wikipedia.org/wiki/Participation_criterion


	!{ winner() != f} {!vote} {winner=f}
	!exists state s
	(!vote(x,f,s,t) on state s => winner()=f)
	And
	(vote(x,f,s,t) on state s => winner()!=f)


	for every state s
	!(!vote(x,f,s,t) => winner()=f)
	or
	!(vote(x,f,s,t) && winner()!=f)


*/
	rule participationCriterion(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		address w1 =  winner();
		require points(w1) >=  points(f);
		require points(w1) >=  points(s);
        require points(w1) >=  points(t);
        vote(e,f,s,t);
		address w2 =  winner();
		assert w1==f => w2==f, "winner changed unexpectly";
	}



