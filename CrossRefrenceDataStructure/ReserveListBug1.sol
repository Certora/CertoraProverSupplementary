pragma solidity ^0.8.7;

contract ReserveList{
    struct ReserveData{
        uint256 id;
        address token;
        uint256 fee;
    }

    mapping(address => ReserveData) internal reserves;
    mapping(uint256 => address) internal underlyingList;
    uint16 internal reserveCount=0;
    function getToken(uint256 index) public view returns (address){
        return underlyingList[index];
    }

    function getIdOfToken(address token) public view returns (uint256){
        return reserves[token].id;
    }

    function getReserveCount() public view returns (uint256){
        return reserveCount;
    }
    function addReserve(address token,uint256 fee) public{
        bool alreadyAdded = reserves[token].id != 0 || underlyingList[0] == token;
        require(!alreadyAdded, "reserve is already in the database");
        reserves[token] = ReserveData({
            id: 0,
            token: token,
            fee: fee
        });
        for(uint16 i =0; i < reserveCount; i++){
            if(underlyingList[i] == address(0)){
                reserves[token].id = i;
                underlyingList[i] = token;
                reserveCount = reserveCount +1;
                //return;
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
        reserveCount = reserveCount -1;
    }
}