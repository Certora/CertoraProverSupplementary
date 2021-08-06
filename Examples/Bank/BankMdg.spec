pragma specify 0.1

using Address as stdlib

/* The only interesting state are the funds, which are returned by getFunds.
 * State transitions are constrained by the following:
 *  - [getFunds_monotonic] getFunds(a) can only be decreased by withdrawals or transfers initiated by a
 *  - [getFunds_positive]  getFunds(a) is always positive
 *  - [getFunds_stable]    *getFunds(a) can only be increased by deposit by a or transfer to a
 *  - [getFunds_funded]    *this.balance >= sum over a of getFunds(a)
 */

methods {
    deposit(uint256)
        /* [dep_success] deposit by a of amt succeeds if
            - message value is at least amt
            - sender's getFunds + amt does not overflow
            - amt + this.balance does not overflow
            */
        /* successful deposit by a of amt has the following effects:
            - [dep_correct]  a's getFunds increase by amt
            */

    withdraw()
        returns bool
        /* [withdraw_success] withdraw by a always succeeds */
        /* successful withdraw by a has the following effects:
            - [withdraw_pays] a message with value (a's getFunds) is sent to a
            - [withdraw_zero] (a's getFunds are set to 0) */
        /* [withdraw_return] withdraw returns ...? (same as a.send) */

    transfer(address,uint256)
        /* [transfer_success] transfer by a to b of amt succeeds if
            - a's getFunds are at least amt
            - b's getFunds + amt does not overflow
            */
        /* successful transfer has the following effects:
            - [transfer_increase] b's getFunds are increased by at least amt
            - [transfer_decrease] a's getFunds are decreased by no more than amt
            */

    getFunds(address account)
        /* [getFunds_success] always succeeds */
        returns (uint256)
        /* [getFunds_return]  returns getFunds(a) */
        envfree

    getTotalFunds() returns(uint256)
        /* [total_success] always succeeds */
        /* [total_correct] returns the sum over a of getFunds(a) */
        envfree
}

// state transitions //////////////////////////////////////////////////////////////

rule getFunds_monotonic(method f) {
    env e;
    calldataarg args;
    address a;

    mathint getFunds_before = getFunds(a);
    f(e,args);
    mathint getFunds_after  = getFunds(a);

    require getFunds_after < getFunds_before;

    assert f.selector != withdraw().selector
        || f.selector != transfer(address,uint256).selector,
        "unauthorized method reduced getFunds";

    assert e.msg.sender == a,
        "unauthorized sender reduced getFunds";
}

invariant getFunds_positive(address a)
    getFunds(a) >= 0

rule getFunds_stable(method f) {
    env e;
    calldataarg args;
    address a;

    mathint getFunds_before = getFunds(a);
    f(e,args);
    mathint getFunds_after  = getFunds(a);

    require getFunds_after > getFunds_before;

    assert f.selector == deposit(uint256).selector
        || f.selector == transfer(address,uint256).selector,
        "unauthorized method increased getFunds";

    assert f.selector == deposit(uint256).selector
        => a == e.msg.sender;

    assert f.selector == transfer(address,uint256).selector
        => false,
        "TODO: check that first argument is a. Can I destructure calldataargs?";
}

invariant getFunds_funded(env e)
    forall address a.
        getTotalFunds() <= stdlib.balance(e, currentContract)
    // TODO: this doesn't quite match English description of getTotalFunds is incorrect

// deposit /////////////////////////////////////////////////////////////////////

rule dep_success() {
    env e;
    uint256 amount;

    require e.msg.value >= amount;
    require getFunds(e.msg.sender) + amount <= max_uint256;
    require getTotalFunds()        + amount >= amount;

    deposit@withrevert(e,amount);
    assert !lastReverted,
           "valid deposit failed";
}

rule dep_correct() {
    env e;
    uint256 amount;

    mathint getFunds_before = getFunds(e.msg.sender);
    deposit(e,amount);
    mathint getFunds_after  = getFunds(e.msg.sender);

    assert getFunds_after == getFunds_before + amount;
}

// withdraw ////////////////////////////////////////////////////////////////////

rule withdraw_success() {
    env e;
    withdraw@withrevert(e);
    assert !lastReverted;
}

rule withdraw_pays() {
    env e;

    mathint balance_before = stdlib.balance(e, e.msg.sender);
    mathint funds_before   = getFunds(e.msg.sender);

    withdraw(e);

    mathint balance_after = stdlib.balance(e, e.msg.sender);

    assert balance_after >= balance_before + funds_before,
        "withdrawal did not successfully increase balance";
}

rule withdraw_zero() {
    env e;

    withdraw(e);
    assert getFunds(e.msg.sender) == 0,
        "withdraw by $e.msg.sender does not drain their funds";
}

rule withdraw_return() {
    assert false, "TODO: rule not implemented";
}

// transfer ////////////////////////////////////////////////////////////////////

rule transfer_todo() {
    assert false, "TODO: transfer rules not yet encoded";
}

// getFunds ////////////////////////////////////////////////////////////////////

rule getFunds_todo() {
    assert false, "TODO: getFunds rules not yet encoded";
}

// getTotalFunds ///////////////////////////////////////////////////////////////

rule getTotalFunds_todo() {
    assert false, "TODO: getTotalFunds rules not yet encoded";
}
