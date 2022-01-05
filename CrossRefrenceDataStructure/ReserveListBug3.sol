pragma solidity ^0.8.7;
import "./IReserveList.sol";

contract ReserveListBug3 is IReserveList{

    mapping(address => ReserveData) private reserves;
    mapping(uint256 => address) private underlyingList;
    uint16 private reserveCount = 0;

    function getTokenAtIndex(uint256 index) external view returns (address) {
        return underlyingList[index];
    }

    function getIdOfToken(address token) external view returns (uint256) {
        return reserves[token].id;
    }

    function getReserveCount() external view returns (uint256) {
        return reserveCount;
    }

    function addReserve(address token, uint256 fee) external {
        bool alreadyAdded = reserves[token].id != 0 ||
            underlyingList[0] == token;
        require(!alreadyAdded, "reserve is already in the database");
        reserves[token] = ReserveData({id: 0, token: token, fee: fee});
        for (uint16 i = 0; i < reserveCount; i++) {
            if (underlyingList[i] == address(0)) {
                reserves[token].id = i;
                underlyingList[i] = token;
                reserveCount = reserveCount + 1;
                return;
            }
        }
        reserves[token].id = reserveCount;
        underlyingList[reserveCount] = token;
        reserveCount = reserveCount + 1;
    }

    function removeReserve(address token) external {
        ReserveData memory reserve = reserves[token];
        //underlyingList[reserves[token].id] = address(0);
        delete reserves[token];
        reserveCount = reserveCount - 1;
    }
}
