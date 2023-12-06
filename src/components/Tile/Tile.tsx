// Importing the CSS file for styling the Tile component
import "./Tile.css";

// Defining the Props interface for the Tile component
interface Props {
  image?: string; // Optional image prop
  number: number; // Required number prop
}

// Exporting the Tile component as the default export
export default function Tile({ number, image }: Props) {
  // Checking if the number is even to determine the tile color
  if (number % 2 === 0) {
    // Rendering the black tile if the number is even
    return (
      <div className="tile black-tile">
        {image && (
          <div
            style={{ backgroundImage: `url(${image})` }}
            className="chess-piece"
          ></div>
        )}
      </div>
    );
  } else {
    // Rendering the white tile if the number is odd
    return (
      <div className="tile white-tile">
        {image && (
          <div
            style={{ backgroundImage: `url(${image})` }}
            className="chess-piece"
          ></div>
        )}
      </div>
    );
  }
}
