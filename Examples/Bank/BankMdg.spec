pragma specify 0.1

methods {
    ghost funds(account) returns mathint
        /*
         * [funds_monotonic] funds(a) can only be decreased by withdrawal or transfer by a
         * [funds_positive]  funds(a) is always positive
         * [funds_stable]    (funds(a) can only be increased by deposit by a or transfer to a)
         * [funds_balance]   (balance is >= sum over a of funds(a))
         */

    deposit(uint256)
        public payable
        /* [dep_success] deposit by a of amt succeeds if
            - message value is at least amt
            - sender's funds + amt does not overflow
            - amt + this.balance does not overflow
            */
        /* successful deposit by a of amt has the following effects:
            - [dep_increase] a's funds increase
            - [dep_correct]  a's funds increase by amt
            */

    withdraw()
        public
        /* [withdraw_success] withdraw by a always succeeds */
        /* successful withdraw by a has the following effects:
            - [withdraw_pays] a message with value (a's funds) is sent to a
            - [withdraw_zero] (a's funds are set to 0) */

        returns bool
        /* [withdraw_return] withdraw returns ...? (same as a.send) */

    transfer(account,uint256)
        public
        /* [transfer_success] transfer by a to b of amt succeeds if
            - a's funds are at least amt
            - b's funds + amt does not overflow
            */
        /* successful transfer has the following effects:
            - [transfer_increase] b's funds are increased by at least amt
            - [transfer_decrease] a's funds are decreased by no more than amt
            */

    getFunds(address account)
        public view
        /* [getFunds_success] always succeeds */
        returns (uint256)
        /* [getFunds_return]  returns funds(a) */
        envfree

    getTotalFunds(address account)
        public view
        /* [total_success] always succeeds */
        returns(uint256)
        /* [total_correct] returns the sum over a of funds(a) */
        envfree
}
