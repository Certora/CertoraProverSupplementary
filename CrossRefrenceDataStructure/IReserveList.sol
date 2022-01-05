interface IReserveList {
    struct ReserveData {
        uint256 id;
        address token;
        uint256 fee;
    }

    function getTokenAtIndex(uint256 index) external view returns (address);
    function getIdOfToken(address token) external view returns (uint256);
    function getReserveCount() external view returns (uint256);

    function addReserve(address token, uint256 fee) external;
    function removeReserve(address token) external;
}