pragma specify 0.1
methods {
	init_state() 
	points(address) returns uint256  envfree
 	voted(address) returns bool  envfree
	winner() returns address envfree
	pointsOfWinner() returns uint256 envfree
}

/*
Emptiness:
	When no user has voted than all candidates have zero votes
	(∀address x ㄱvoted(x))  (∀address c  points(c)=0)
*/
	invariant  emptiness() (forall address x. !sinvoke voted(x) ) => (forall address c. sinvoke points(c)==0)

/*
Integrity of voted:
	Once a user issue a vote operation he is marked as voted globally (for all next states)
	vote(x,f,s,t)  Globally voted(x) 
*/
	rule golballyVoted(address x, method f) {
		require sinvoke voted(x);
		env eF;
		calldataarg arg; 
		sinvoke f(eF,arg); 
		assert (sinvoke voted(x));
	}
	
	rule integerityVote(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		sinvoke  vote(e,f,s,t);
		assert (sinvoke voted(x));
	}

/*
Single vote per user
	A user can not vote if he has voted before
 	voted(x)  ㄱvote(x,f,s,t)  
*/
	rule singleVote(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		bool before = sinvoke voted(x);
		invoke  vote(e,f,s,t);
		assert before => lastReverted; 
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
		uint256  f_points = sinvoke points(f);
		uint256  s_points = sinvoke points(s);
		uint256  t_points = sinvoke points(t);
		sinvoke  vote(e,f,s,t);
		assert ( sinvoke points(f) == f_points +3 &&
				sinvoke points(s) == s_points +2 &&
				sinvoke points(t) == t_points +1 ); 
	}


/*
No effect on other candidates:
	∀address c, c≠{f,s,t}. 
	{c_points = points(c)}  vote(x,f,s,t) {points(c) = c_points}
*/

	rule noEffect(address x, address f, address s, address t) {
		env e;
		address c;
		require(x==e.msg.sender);
		require( c!=f &&  c!=s  && c!=t);
		uint256  c_points = sinvoke points(c);
		sinvoke  vote(e,f,s,t);
		assert ( sinvoke points(c) == c_points ); 
	}



/*
No effect on unsuccessful vote operation
	∀address c,y. 
	{c_points = points(c) ⋀  b = voted(y)}  
	ㄱvote(x,f,s,t) 
	{points(c) = c_points ⋀ voted(y) = b} 
 */
	rule noEffect(address x, address f, address s, address t) {
		env e;
		address c;
		address y;
		require(x==e.msg.sender);
		uint256  c_points = sinvoke points(c);
		bool y_voted = sinvoke voted(y);
		invoke  vote(e,f,s,t);
		require(lastReverted);
		assert ( sinvoke points(c) == c_points && sinvoke voted(y) == y_voted); 
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
		sinvoke  vote(e1,f1,s1,t1);
		sinvoke  vote(e2,f2,s2,t2);
		uint256  c_points_P1 = sinvoke points(c);
		bool y_voted_P1 = sinvoke voted(y);
		address w1 = sinvoke winner();
		sinvoke  vote(e2,f2,s2,t2) at init;
		sinvoke  vote(e1,f1,s1,t1);
		uint256  c_points_P2 = sinvoke points(c);
		bool y_voted_P2 = sinvoke voted(y);
		address w2 = sinvoke winner();
		assert ( c_points_P1 == c_points_P2 &&  y_voted_P1 == y_voted_P2); 
		//assert (w1 == w2); //we can not demand this the order is imporant in case of a tie 

	}
/*
 Integrity of winner
	The winner has the most points 
	winner() = w  ∀address c. points(c) ≤  points(w)
*/
 invariant integrityWinner(address w)
 	sinvoke winner() == w => (forall address c. sinvoke points(w) >= sinvoke points(c))

/*
Resolvability criterion
	For every (possibly tied) winner in a result, there must exist a way for one added vote to make that winner unique
	https://en.wikipedia.org/wiki/Resolvability_criterion
	∃address f,s,t
	{∃address c, c≠winner() ⋀ points(winner()) = points(c) } vote(x,f,s,t) { ∀address c. points(c) < points(winner()) } 
*/
	/**** this should fail ************/
	rule resolvabilityCriterion(address x, address f, address s, address t) {
		env e;
		require(x==e.msg.sender);
		address w = sinvoke winner();
		address c;
		require (c!=w);
		require ( sinvoke points(c) == sinvoke points(w));
		//the following does not pass:
		//assert (exists address f. exists address s. exists address t. sinvoke  vote(e,f,s,t) &&  (forall address c1. sinvoke points(c1) < sinvoke pointsOfWinner()));
		//if this fail then we found an exists
		
		sinvoke  vote(e,f,s,t);
		address w1 = sinvoke winner();
		address c1; 
		// this is not the same, it finds a state and for that state it finds an option to get out of the tie.
		// It does not implies that for every possible tie exsist a vote that will change to unique winner
		assert ( c1!= w1 => sinvoke points(c1) < sinvoke pointsOfWinner());
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
		address w1 = sinvoke winner();
		//safe assumption intgerity of winner 
		assert(forall address c. (sinvoke points(w1) >= sinvoke points(c))); //todo - this is not working
		sinvoke  vote(e,f,s,t);
		address w2 = sinvoke winner();
		assert( w1==f => w2==f);
		assert false;
	}


/*
Later-no-harm criterion (expected violation)
a voter giving an additional ranking or positive rating to a less-preferred candidate can not cause a more-preferred candidate to lose

		{f=winner} vote(x,f,s,t) {f=winner()}
*/
	/**** this should fail ********/
	rule laterNoHarmCriterion(address x, address f, address s, address t, address s2, address t2) {
		env e;
		require(x==e.msg.sender);
		storage init = lastStorage; 
		sinvoke  vote(e,f,s,t); 
		address w1 = sinvoke winner();
		// by changing second and third voter, we did not cause f to lose
		sinvoke  vote(e,f,s2,t2) at init;
		address w2 = sinvoke winner();
		assert ( w1 == f => w2 == f) ;
		
	}

