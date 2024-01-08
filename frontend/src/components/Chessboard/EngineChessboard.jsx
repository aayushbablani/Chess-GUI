import React, { useState } from "react";
import Chessboard from "../Referee/Referee";
import './EngineChessboard.css'
import Referee from "../Referee/Referee";

function EngineChessboard() {
    return(
        <div className="EngineFullContainer">
            <EngineSelection />
            <Referee />
        </div>
    )
}

function EngineSelection() {

  const [selectedColor, setSelectedColor] = useState(null);
  const [selectedTimeControl, setSelectedTimeControl] = useState(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState(null);

  const handlePlayButtonClick = () => {
    // Add your logic for starting the game with selected options
    console.log('Selected Color:', selectedColor);
    console.log('Selected Time Control:', selectedTimeControl);
    console.log('Selected Difficulty:', selectedDifficulty);
  };

  return (
    <div className="EngineSelectionContainer">
      <ColorSelection onSelectColor={setSelectedColor} />
      <TimeControlSelection onSelectTimeControl={setSelectedTimeControl} />
      <DifficultySelection onSelectDifficulty={setSelectedDifficulty} />
      <button className="EnginePlayButton" onClick={handlePlayButtonClick}>Play</button>
    </div>
  );

}

const ColorSelection = ({ onSelectColor }) => {
    return (
      <div>
        <h3 className="EngineSelectHeader">Select Color</h3>
          <button className="EngineColorButtonWhite" onClick={() => onSelectColor('white')}>White</button>
          <button className="EngineColorButtonBlack" onClick={() => onSelectColor('black')}>Black</button>
      </div>
    );
};

const TimeControlSelection = ({ onSelectTimeControl }) => {

  return (
    <div>
      <h3 className="EngineSelectHeader">Time Control</h3>
      <button className="EngineColorButtons" onClick={() => onSelectTimeControl('1 min')}>1 min</button>
      <button className="EngineColorButtons" onClick={() => onSelectTimeControl('5 min')}>5 min</button>
      <button className="EngineColorButtons" onClick={() => onSelectTimeControl('15 min')}>15 min</button>
      <button className="EngineColorButtons" onClick={() => onSelectTimeControl('60 min')}>60 min</button>
    </div>
  );
};

const DifficultySelection = ({ onSelectDifficulty }) => {
  return (
    <div>
      <h3 className="EngineSelectHeader">Select Difficulty</h3>
      <button className="EngineColorButtons" onClick={() => onSelectDifficulty(800)}>800</button>
      <button className="EngineColorButtons" onClick={() => onSelectDifficulty(1400)}>1400</button>
      <button className="EngineColorButtons" onClick={() => onSelectDifficulty(2000)}>2000</button>
      <button className="EngineColorButtons" onClick={() => onSelectDifficulty(2600)}>2600</button>
    </div>
  );
};

export default EngineChessboard;