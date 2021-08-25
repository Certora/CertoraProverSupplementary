// finds the popsicle bug
rule increase_total_value_without_actually_adding_assets(method f) filtered { f -> f.selector != deposit().selector &&  f.selector != OwnerDoItsJobAndEarnsFeesToItsClients().selector && !f.isFallback }  {
    env e;
    require(numAccounts(e) == 2);
    total_balance_before = assetsOf(e, a) + assetsOf(e, b);
    address a = getUser(e, 0);
    address b = getUser(e, 1);
    f(e, all_args);
    total_balance_after = assetsOf(e, a) + assetsOf(e, b);
    assert (total_balance_after <= total_balance_before, 
            "error - deposit / OwnerDoItsJobAndEarnsFeesToItsClients aren't used thus users assets may only decrease") 
}