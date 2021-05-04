methods {
	counter() returns uint256 envfree
}

rule invertible {
	uint256 curr = counter();
	/* The `env` type represents the EVM parameters passed in every
	   call (msg., tx., block.* variables in Solidity)
	 */
	env e;  
	/* For non-`envfree` methods, the environment must be passed as the first argument*/
	inc(e);
	dec(e);
	assert counter() == curr, "dec followed by inc should give the original value";
}

rule monotone {
	uint256 curr = counter();
	env e;  
	assert inc(e) > curr, "Incremented value is greater than original value";
}