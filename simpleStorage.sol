//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract simpleStorage {
    uint256 favNumber;

    struct people {
        string name;
        uint256 age;
    }

    people[] public peopleArr;
    mapping(string => uint256) public nameToAge;

    function storeNumber(uint256 x) public returns (uint256) {
        favNumber = x;
        return x;
    }

    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    function addPerson(string memory _name, uint256 _age) public {
        peopleArr.push(people(_name, _age));
        nameToAge[_name] = _age;
    }
}
