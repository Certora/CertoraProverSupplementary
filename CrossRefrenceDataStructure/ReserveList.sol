pragma solidity ^0.8.7;

contract ReserveList{
    struct ReserveData{
        uint256 id;
        address token;
    }

    mapping(address => ReserveData) internal reserves;
    mapping(uint256 => address) internal underlyingList;
    uint256 internal reserveCount;


    function addReserve(address token) public{
        bool alreadyAdded = reserves[token].id != 0 || underlyingList[0] == token;
        require(!alreadyAdded, "reserve is already in the database");
        for(uint16 i =0; i<reserveCount; ++i){
            if(underlyingList[i] = address(0)){
                reserves[token].id = i;
                underlyingList[i] = token;
                return;
            }
        }
        reserves[token].id = reserveCount;
        underlyingList[reserveCount] = token;
        reserveCount = reserveCount + 1;
    }
    function removeReserve(address token) public{
        ReserveData memory reserve = reserves[token];
        underlyingList[reserves[token].id] = address(0);
        delete reserves[token];
    }
}