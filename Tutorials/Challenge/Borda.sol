pragma solidity >= 0.6.0;

/* Do not change BordaInterface */
interface BordaInterface {

    // current winner
    function winner() external view returns(address);

    // msg.sender votes first choice to f, second to s and third to t
    function vote(address f, address s, address t) external;

    // number of points the candidate has received
    function points(address c) external view returns(uint256);

    // has user x voted?
    function voted(address x) external view returns(bool);
}

/* Feel free to change any code below this point */

library SafeMath {
    function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

    function safeSub(uint256 x, uint256 y) internal pure returns(uint256) {
        assert(x >= y);
        uint256 z = x - y;
        return z;
    }
}

contract Borda is BordaInterface{
    using SafeMath for uint256;

    // The current winner
    address public _winner;

    // A map storing whether an address has already voted. Initialized to false.
    mapping (address => bool)  _voted;

    // Points each candidate has recieved, initialized to zero.
    mapping (address => uint256) _points;

    // current max points of all candidates.
    uint256 public pointsOfWinner;


    function vote(address f, address s, address t) public override {
        require(!_voted[msg.sender], "this voter has already cast its vote");
        require( f != s && f != t && s != t, "candidates are not different");
        _voted[msg.sender] = true;
        voteTo(f, 3);
        voteTo(s, 2);
        voteTo(t, 1);
    }

    function voteTo(address c, uint256 p) private {
        //update points
        _points[c] = _points[c].safeAdd(p);
        // update winner if needed
        if (_points[c] > _points[_winner]) {
            _winner = c;
        }
    }

    function winner() external view override returns (address) {
        return _winner;
    }

    function points(address c) public view override returns (uint256) {
        return _points[c];
    }

    function voted(address x) public view override returns(bool) {
        return _voted[x];
    }

    function init_state() public {}

}
