pragma solidity ^0.5.12;

contract LinearSearch {
  uint256[] public entries;

  function getNumEntries() public view returns (uint256) {
    return entries.length;
  }

  function indexOf(uint256 value) public returns (bool, uint256) {
    for (uint256 i = 0; i < entries.length; i++) {
      if (entries[i] == value) {
        return (true, i);
      }
    }

    return (false, uint256(-1));
  }
}
