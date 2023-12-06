import { PieceType, TeamType, Piece } from "../Chessboard/Chessboard";

export default class Referee {
  tileIsOccupied(x: number, y: number, board: Piece[]): boolean {
    const piece = board.find((piece) => piece.x === x && piece.y === y);
    if (piece) {
      return true;
    } else {
      return false;
    }
  }

  tileIsOccupiedByTeam(
    x: number,
    y: number,
    team: TeamType,
    board: Piece[]
  ): boolean {
    const piece = board.find(
      (piece) => piece.x === x && piece.y === y && piece.team !== team
    );
    if (piece) {
      return true;
    } else {
      return false;
    }
  }

  isValidMove(
    px: number,
    py: number,
    x: number,
    y: number,
    type: PieceType,
    team: TeamType,
    board: Piece[]
  ) {
    if (type === PieceType.Pawn) {
      const specialRow = team === TeamType.Player ? 1 : 6;
      const pawnDirection = team === TeamType.Player ? 1 : -1;
      if (py === specialRow && px === x && y - py === 2 * pawnDirection) {
        if (
          !this.tileIsOccupied(x, y, board) &&
          !this.tileIsOccupied(x, y - pawnDirection, board)
        ) {
          return true;
        }
      } else if (px === x && y - py === pawnDirection) {
        if (!this.tileIsOccupied(x, y, board)) {
          return true;
        }
      }
      else if (x - px === -1 && y - py === pawnDirection) {
        if (this.tileIsOccupiedByTeam(x, y, team, board)) {
          console.log("Attack in the upper or bottom left corner");
          return true;
        }
      } else if (x - px === 1 && y - py === pawnDirection) {
        if (this.tileIsOccupiedByTeam(x, y, team, board)) {
          console.log("Attack in the upper or bottom right corner");
          return true;
        }
      }
    }

    if (type === PieceType.Bishop) {
      if (Math.abs(x - px) === Math.abs(y - py)) { // Check if move is diagonal
        const xDirection = x > px ? 1 : -1;
        const yDirection = y > py ? 1 : -1;
    
        let checkX = px + xDirection;
        let checkY = py + yDirection;
    
        // Check each square along the diagonal, excluding the final tile
        while (checkX !== x - xDirection || checkY !== y - yDirection) {
          if (this.tileIsOccupied(checkX, checkY, board)) {
            return false; // Another piece is in the way
          }
          checkX += xDirection;
          checkY += yDirection;
        }
    
        // Check if the final destination tile is occupied by an opponent's piece
        if (this.tileIsOccupied(x, y, board) && this.tileIsOccupiedByTeam(x, y, team, board)) {
          return true; // Capturing an opponent's piece
        } else if (!this.tileIsOccupied(x, y, board)) {
          return true; // Move to an empty square
        }
      }
      return false; // Move is not diagonally valid
    }

    if (type === PieceType.Rook) {
      // Horizontal movement (y coordinates remain the same)
      if (py === y) {
        const xDirection = x > px ? 1 : -1;
        for (let checkX = px + xDirection; checkX !== x; checkX += xDirection) {
          if (this.tileIsOccupied(checkX, y, board)) {
            return false; // Another piece is in the way
          }
        }
      } 
      // Vertical movement (x coordinates remain the same)
      else if (px === x) {
        const yDirection = y > py ? 1 : -1;
        for (let checkY = py + yDirection; checkY !== y; checkY += yDirection) {
          if (this.tileIsOccupied(px, checkY, board)) {
            return false; // Another piece is in the way
          }
        }
      } else {
        return false; // Rook can't move diagonally
      }
    
      // Check if the destination tile is occupied by an opponent's piece
      if (this.tileIsOccupied(x, y, board) && this.tileIsOccupiedByTeam(x, y, team, board)) {
        return true; // Capturing an opponent's piece
      } else if (!this.tileIsOccupied(x, y, board)) {
        return true; // Move to an empty square
      }
      return false; // Destination square is blocked by a piece of the same team
    }

    if (type === PieceType.Knight) {
      // Calculate the absolute difference in x and y coordinates
      const dx = Math.abs(x - px);
      const dy = Math.abs(y - py);
    
      // Check for L-shape movement (2 squares in one direction, 1 square in another)
      if ((dx === 2 && dy === 1) || (dx === 1 && dy === 2)) {
        // Check if the destination tile is occupied by an opponent's piece or empty
        if (this.tileIsOccupied(x, y, board) && this.tileIsOccupiedByTeam(x, y, team, board)) {
          return true; // Capturing an opponent's piece
        } else if (!this.tileIsOccupied(x, y, board)) {
          return true; // Move to an empty square
        }
      }
      return false; // Any other movement is invalid for a Knight
    }

    if (type === PieceType.Queen) {
      // Combining the logic of Rook and Bishop
    
      // Horizontal or Vertical movement (like Rook)
      if (px === x || py === y) {
        const xDirection = px === x ? 0 : x > px ? 1 : -1;
        const yDirection = py === y ? 0 : y > py ? 1 : -1;
    
        let checkX = px + xDirection;
        let checkY = py + yDirection;
    
        while (checkX !== x || checkY !== y) {
          if (this.tileIsOccupied(checkX, checkY, board)) {
            return false; // Another piece is in the way
          }
          checkX += xDirection;
          checkY += yDirection;
        }
      } 
      // Diagonal movement (like Bishop)
      else if (Math.abs(x - px) === Math.abs(y - py)) {
        const xDirection = x > px ? 1 : -1;
        const yDirection = y > py ? 1 : -1;
    
        let checkX = px + xDirection;
        let checkY = py + yDirection;
    
        while (checkX !== x - xDirection || checkY !== y - yDirection) {
          if (this.tileIsOccupied(checkX, checkY, board)) {
            return false; // Another piece is in the way
          }
          checkX += xDirection;
          checkY += yDirection;
        }
      } else {
        return false; // Invalid movement for a Queen
      }
    
      // Check if the destination tile is occupied by an opponent's piece
      if (this.tileIsOccupied(x, y, board) && this.tileIsOccupiedByTeam(x, y, team, board)) {
        return true; // Capturing an opponent's piece
      } else if (!this.tileIsOccupied(x, y, board)) {
        return true; // Move to an empty square
      }
      return false; // Destination square is blocked by a piece of the same team
    }
    
    if (type === PieceType.King) {
      // Calculate the absolute difference in x and y coordinates
      const dx = Math.abs(x - px);
      const dy = Math.abs(y - py);
    
      // Check for single-square movement in any direction
      if ((dx === 1 && dy <= 1) || (dy === 1 && dx <= 1)) {
        // Check if the destination tile is occupied by an opponent's piece or empty
        if (this.tileIsOccupied(x, y, board) && this.tileIsOccupiedByTeam(x, y, team, board)) {
          return true; // Capturing an opponent's piece
        } else if (!this.tileIsOccupied(x, y, board)) {
          return true; // Move to an empty square
        }
      }
      return false; // Any other movement is invalid for a King
    }
    return false;
    
  }
  
}
