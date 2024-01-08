import React, { useState } from "react";
import Chessboard from "../Referee/Referee";
import './FriendChessboard.css'
import Referee from "../Referee/Referee";

function FriendChessboard() {

    const [playClicked, setPlayClicked] = useState(false);

    const StartMatch = () => {
        setPlayClicked(true);
    };

    function FriendSelection() {

        const [selectedColor, setSelectedColor] = useState(null);
        const [selectedTimeControl, setSelectedTimeControl] = useState(null);

        const handlePlayButtonClick = () => {
            // Add your logic for starting the game with selected options
            console.log('Selected Color:', selectedColor);
            console.log('Selected Time Control:', selectedTimeControl);
            StartMatch();
        };

        return (
            <div className="FriendSelectionContainer">
                <ColorSelection onSelectColor={setSelectedColor} />
                <TimeControlSelection onSelectTimeControl={setSelectedTimeControl} />
                <button className="FriendPlayButton" onClick={handlePlayButtonClick}>Play</button>
            </div>
        );

    }

    const ColorSelection = ({ onSelectColor }) => {
        return (
            <div>
                <h3 className="FriendSelectHeader">Select Color</h3>
                <button className="FriendColorButtonWhite" onClick={() => onSelectColor('white')}>White</button>
                <button className="FriendColorButtonBlack" onClick={() => onSelectColor('black')}>Black</button>
            </div>
        );
    };

    const TimeControlSelection = ({ onSelectTimeControl }) => {
        return (
            <div>
                <h3 className="FriendSelectHeader">Time Control</h3>
                <button className='FriendColorButtons' onClick={() => onSelectTimeControl('1 min')}>1 min</button>
                <button className="FriendColorButtons" onClick={() => onSelectTimeControl('5 min')}>5 min</button>
                <button className="FriendColorButtons" onClick={() => onSelectTimeControl('15 min')}>15 min</button>
                <button className="FriendColorButtons" onClick={() => onSelectTimeControl('60 min')}>60 min</button>
            </div>
        );
    };

    return(
        <div className="FriendFullContainer">
            {!playClicked && (
                <>
                    <FriendSelection />
                </>
            )}
            <Referee />
        </div>
    )

}

export default FriendChessboard;