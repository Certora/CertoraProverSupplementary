rule checkUnintialized(method f){
    env e;
    calldataarg args;
    
    f(e, args);

}