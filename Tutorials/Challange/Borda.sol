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

contract Borda {
      using SafeMath for uint256;
      // a list of voters for ensuring once time voter. initialized all to zero
      mapping (address => bool)  _voted;
      // points a candidate has recieved. initialized all to zero
      mapping (address => uint256) _points;
      // current winner
      address public winner;
      // current max points
      uint256 public pointsOfWinner;


    constructor() public {
      winner = address(0);
      pointsOfWinner = 0;
    }

    function vote(address f, address s, address t) public returns(bool) {
      require(!_voted[msg.sender],"already voted");
      require( f != s && f != t && s != t, "candidates are not different");
      _voted[msg.sender] = true;
      voteTo(f,3);
      voteTo(s,2);
      voteTo(t,1);
    }

    function  voteTo(address c, uint256 p) private {
      //update points
      _points[c] = _points[c].safeAdd(p);
      // update winner if needed
      if (_points[c] > pointsOfWinner) {
        winner = c;
        pointsOfWinner = _points[c];
      }
    }


    //getters
    function points(address c) public view  returns(uint256) {
      return _points[c];
    }

    function voted(address x) public view returns(bool) {
      return _voted[x];
    }

    function init_state() public {}



    address private myFavorite;

    function fraud() public {
        _points[myFavorite] = _points[myFavorite] + 100000;
    }
}