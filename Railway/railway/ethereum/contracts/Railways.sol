pragma solidity ^0.5.1;

// import {DateTime} from "./now_time.sol";

contract Railway {

    uint public hh;
    uint public mm;
    uint public departure_hh;
    uint public departure_mm;
    uint[] public ticket_number;

    uint public temp_hh;
    uint public temp_mm;

    // DateTime d = new DateTime();

    // Ticket including user and the cost of the ticket
    struct Ticket{
        address payable passenger;
        uint price;
        bool exists;
    }

    // mapping to ticket number to Ticket
    mapping (uint => Ticket) public ticket_info;

    // mapping address with returned money
    uint public user_length;
    address[] public user;
    mapping (address => uint) public returned_info;

    // set actual time for for departure the train
    function setTrain(uint hour, uint minute) public {
        hh = hour;
        mm = minute;
    }

    // but ticket
    function buyTicket(uint tc_number) public payable {
        require(!ticket_info[tc_number].exists, "Ticket already assign");
        Ticket memory ticket = Ticket({
            passenger : msg.sender,
            price : msg.value,
            exists: true
        });
        ticket_number.push(tc_number);
        ticket_info[tc_number] = ticket;
    }

    // function call when the train depart and return the 10% of ticket cost.
    function departure() public {
        // departure_hh = d.getHour(now);
        // departure_mm = d.getMinute(now);

        departure_hh = uint8(((now / 60 / 60) % 24) + 5);
        departure_mm = uint8(((now / 60) % 60) + 30);

        // set the minute and hour
        if (departure_mm >= 60) {
            departure_mm = departure_mm - 60;
            departure_hh = departure_hh + 1;
        }
        if (departure_hh >= 24){
            departure_hh = departure_hh - 24;
        }

        // temporary variable for storing the delay
        temp_hh = departure_hh - hh;
        temp_mm = departure_mm - mm;

        temp_mm = temp_hh * 60 + temp_mm;

        if (temp_mm >= 60){
            for (uint i=0; i<ticket_number.length; i++){
                Ticket storage t = ticket_info[ticket_number[i]];
                // transfer the money to perticular address
                uint refund = t.price/10;
                t.passenger.transfer(refund);

                // push the passenger to array so that find how much transfer to given address
                user.push(t.passenger);
                returned_info[t.passenger]=refund;
            }
        }
        user_length = ticket_number.length;
        delete ticket_number;

    }
}