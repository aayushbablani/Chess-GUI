import React, {useState} from 'react';
import './Selection.css'; // Styles for Selection Page
import EngineChessboard from '../Chessboard/EngineChessboard';
import FriendChessboard from '../Chessboard/FriendChessboard';
import Referee from '../Referee/Referee';

function Selection() {

    const [selectedComponent, setSelectedComponent] = useState(null);
    const [chessboardRendered, setChessboardRendered] = useState(false);

    const SelectAgainstEngineBoard = () => {
        setSelectedComponent('engine');
        setChessboardRendered(true);
    };

    const SelectAgainstFriendBoard = () => {
        setSelectedComponent('friend');
        setChessboardRendered(true);
    };

    const SelectAnalysisBoard = () => {
        setSelectedComponent('analysis');
        setChessboardRendered(true);
    };

    return (

        <div className='selectionContainer'>
            {!chessboardRendered && (
                <div>
                    <div className='versEBcontainer'> {/*Container for player v engine button*/}
                        <button id='versEB' onClick={SelectAgainstEngineBoard}>
                            <img src="assets/images/engine_giraffe.svg" alt="green giraffe as chess piece" width="20%" height="80%"/>
                            <strong>vs Engine</strong>
                        </button> {/* Button for player v engine*/}
                    </div>

                    <div className='versFBcontainer'> {/*Container for player v friend button*/}
                        <button id='versFB' onClick={SelectAgainstFriendBoard}>
                            <img src="assets/images/friend_giraffe.svg" alt="yellow giraffe as chess piece" width="23%" height="85%"/>
                            <strong>vs Friend</strong>
                        </button> {/* Button for player v friend*/}
                    </div>

                    <div className='anaBcontainer'> {/*Container for analysis button*/}
                        <button id='anaB' onClick={SelectAnalysisBoard}>
                            <img src="assets/images/analys_ico.svg" alt="magnifiying glass over chessboard"/>
                            <strong>Analysis</strong>
                        </button> {/* Button for analysis*/}
                    </div>
                </div>
            )}

            {selectedComponent && (
                <div>
                    {selectedComponent === 'engine' && <EngineChessboard />}
                    {selectedComponent === 'friend' && <FriendChessboard />}
                    {selectedComponent === 'analysis' && <Referee />}
                </div>
            )}

        </div>

    );
}

export default Selection;