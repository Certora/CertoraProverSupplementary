certoraRun BorrowSystem.sol:SimpleBorrowSystem DummyERC20A.sol DummyERC20B.sol \
	--link SimpleBorrowSystem:collateralToken=DummyERC20A SimpleBorrowSystem:borrowToken=DummyERC20B \
	--verify SimpleBorrowSystem:BorrowSystem.spec \
	--solc solc8.4 \
	--settings -postProcessCounterExamples=true,-assumeUnwindCond \
	--staging \
	--msg "SimpleBorrowSystem example" 
