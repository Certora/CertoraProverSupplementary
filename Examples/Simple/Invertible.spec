methods {
	counter() returns uint256 envfree
}

rule invertible {
	/* `sinvoke foo(args)` - process function `foo` with arguments `args` 
		and assume that it does not revert */
	uint256 curr = sinvoke counter();
	/* The `env` type represents the EVM parameters passed in every
	   call (msg., tx., block.* variables in Solidity)
	 */
	env e;  
	/* For non-`envfree` methods, the environment is passed as the first argument*/
	sinvoke inc(e);
	sinvoke dec(e);
	assert sinvoke counter() == curr, "dec followed by inc should give the original value";
}

rule monotone {
	uint256 curr = sinvoke counter();
	env e;  
	assert sinvoke inc(e) > curr, "Incremented value is greater than original value";
}