// Import necessary components and styles
import { useRef, useState } from "react";
import Referee from "../Referee/Referee";
import Tile from "../Tile/Tile";
import "./Chessboard.css";

// Define the vertical and horizontal axes of the chessboard
const verticalAxis = ["1", "2", "3", "4", "5", "6", "7", "8"];
const horizontalAxis = ["a", "b", "c", "d", "e", "f", "g", "h"];

// Define the interface for a Piece
export interface Piece {
  image: string;
  x: number;
  y: number;
  type: PieceType;
  team: TeamType;
}

export enum PieceType {
  Pawn,
  Bishop,
  Knight,
  Rook,
  Queen,
  King,
}

export enum TeamType {
  Opps,
  Player,
}

const initialBoardState: Piece[] = [];

// Add pieces to the board for both players
for (let p = 0; p < 2; p++) {
  const teamType = p === 0 ? TeamType.Opps : TeamType.Player;
  const type = teamType === TeamType.Opps ? "b" : "w";
  const y = teamType === TeamType.Opps ? 7 : 0;
  initialBoardState.push({
    image: `images/rook_${type}.png`,
    x: 0,
    y,
    type: PieceType.Rook,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/rook_${type}.png`,
    x: 7,
    y,
    type: PieceType.Rook,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/knight_${type}.png`,
    x: 1,
    y,
    type: PieceType.Knight,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/knight_${type}.png`,
    x: 6,
    y,
    type: PieceType.Knight,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/bishop_${type}.png`,
    x: 2,
    y,
    type: PieceType.Bishop,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/bishop_${type}.png`,
    x: 5,
    y,
    type: PieceType.Bishop,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/queen_${type}.png`,
    x: 3,
    y,
    type: PieceType.Queen,
    team: teamType,
  });
  initialBoardState.push({
    image: `images/king_${type}.png`,
    x: 4,
    y,
    type: PieceType.King,
    team: teamType,
  });
}

// Add pawns for both players
for (let i = 0; i < 8; i++) {
  initialBoardState.push({
    image: "images/pawn_b.png",
    x: i,
    y: 6,
    type: PieceType.Pawn,
    team: TeamType.Opps,
  });
}

for (let i = 0; i < 8; i++) {
  initialBoardState.push({
    image: "images/pawn_w.png",
    x: i,
    y: 1,
    type: PieceType.Pawn,
    team: TeamType.Player,
  });
}

// Chessboard component
export default function Chessboard() {
  const [activePiece, setActive] = useState<HTMLElement | null>(null); // State to store if a piece is active or not
  const [gridX, setGridX] = useState<number>(0); // State to store the x coordinate of the piece
  const [gridY, setGridY] = useState<number>(0); // State to store the y coordinate of the piece
  const [pieces, setPieces] = useState<Piece[]>(initialBoardState); // State to store the pieces on the board
  const chessboardRef = useRef<HTMLDivElement>(null);
  const referee = new Referee();

  function grabPiece(e: React.MouseEvent<HTMLDivElement, MouseEvent>) {
    const chessboard = chessboardRef.current;
    const element = e.target as HTMLDivElement;
    if (element.classList.contains("chess-piece") && chessboard) {
      setGridX(Math.floor((e.clientX - chessboard.offsetLeft) / 100));
      setGridY(
        Math.abs(Math.ceil((e.clientY - chessboard.offsetTop - 800) / 100))
      );

      const x = e.clientX - 50;
      const y = e.clientY - 50;
      element.style.position = "absolute";
      element.style.left = `${x}px`;
      element.style.top = `${y}px`;

      setActive(element);
    }
  }

  function movePiece(e: React.MouseEvent) {
    const chessboard = chessboardRef.current;
    if (activePiece && chessboard) {
      const minX = chessboard.offsetLeft - 25;
      const minY = chessboard.offsetTop - 25;
      const maxX = chessboard.offsetLeft + chessboard.clientWidth - 75;
      const maxY = chessboard.offsetTop + chessboard.clientHeight - 75;
      const x = e.clientX - 50;
      const y = e.clientY - 50;
      activePiece.style.position = "absolute";

      //If x is smaller than minimum amount
      if (x < minX) {
        activePiece.style.left = `${minX}px`;
      }
      //If x is bigger than maximum amount
      else if (x > maxX) {
        activePiece.style.left = `${maxX}px`;
      }
      //If x is in the constraints
      else {
        activePiece.style.left = `${x}px`;
      }

      //If y is smaller than minimum amount
      if (y < minY) {
        activePiece.style.top = `${minY}px`;
      }
      //If y is bigger than maximum amount
      else if (y > maxY) {
        activePiece.style.top = `${maxY}px`;
      }
      //If y is in the constraints
      else {
        activePiece.style.top = `${y}px`;
      }
    }
  }

  function dropPiece(e: React.MouseEvent) {
    const chessboard = chessboardRef.current;
    if (activePiece && chessboard) {
      const x = Math.floor((e.clientX - chessboard.offsetLeft) / 100);
      const y = Math.abs(
        Math.ceil((e.clientY - chessboard.offsetTop - 800) / 100)
      );

      console.log(x, y);

      const currentPiece = pieces.find((p) => p.x === gridX && p.y === gridY);
      const targetPiece = pieces.find((p) => p.x === x && p.y === y);

      if (currentPiece) {
        const validMove = referee.isValidMove(
          gridX,
          gridY,
          x,
          y,
          currentPiece.type,
          currentPiece.team,
          pieces
        );

        if (validMove) {
          // Updates the piece position
          // and removes the piece if there is one on the target tile

          const updatedPieces = pieces.reduce((results, piece) => {
            if (piece === currentPiece) {
              // Update the current piece's position
              results.push({ ...piece, x: x, y: y });
            } else if (!(piece.x === x && piece.y === y)) {
              // Keep other pieces that are not at the target position
              results.push(piece);
            }
            // Implicitly, do not add the piece at the target position (captured piece) to results
            return results;
          }, [] as Piece[]);

          setPieces(updatedPieces);
        } else {
          // Resets the piece position
          activePiece.style.position = "relative";
          activePiece.style.removeProperty("left");
          activePiece.style.removeProperty("top");
        }
      }

      setActive(null);
    }
  }

  let board = [];

  // Generate the chessboard with tiles and pieces
  for (let j = verticalAxis.length - 1; j >= 0; j--) {
    for (let i = 0; i < horizontalAxis.length; i++) {
      const number = j + i + 2;
      let image = undefined;

      // Find the piece for the current tile
      pieces.forEach((p) => {
        if (p.x === i && p.y === j) {
          image = p.image;
        }
      });

      // Add the Tile component to the board
      // eslint-disable-next-line no-template-curly-in-string
      board.push(<Tile key={`${j},${i}`} image={image} number={number} />);
    }
  }

  // Render the chessboard with tiles and pieces
  return (
    <div
      onMouseMove={(e) => movePiece(e)}
      onMouseDown={(e) => grabPiece(e)}
      onMouseUp={(e) => dropPiece(e)}
      id="chessboard"
      ref={chessboardRef}
    >
      {board}
    </div>
  );
}
