// finds the popsicle bug
rule increase_total_value_without_actually_adding_assets(uint amount) {
    env e;
    sync(e);
    transfer_to_pool(a);
    beforeFunds
    add_liquidity(e); 
    afterFunds
    assert afterFunds - beforeFunds <= a;
}