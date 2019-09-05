package game;

public class Tile {

    /** An enum representing the different types of Tiles that may appear in a
     * sewer system.
     * 
     * @author eperdew */
    public enum Type {
        FLOOR, RING, ENTRANCE, WALL {
            @Override public boolean isOpen() {
                return false;
            }
        };
        
        /**  Return true iff this Type of Tile is traversable. */
        public boolean isOpen() {
            return true;
        }
    }

    /** The row and column position of the GameNode */
    private final int row;
    private final int col;

    /** Value of coins on this Node */
    private final int coinValue;
    
    /** The Type of Tile this Node has */
    private Type type;
    private boolean coinsPickedUp;
    
    /** Constructor: an instance with row r, column c, coin-value cv, and Type t. */
    public Tile(int r, int c, int cv, Type t) {
        row= r;
        col= c;
        coinValue= cv;
        type= t;
        coinsPickedUp= false;
    }
    
    /** Return the value of coins on this Tile. */
    public int coins() {
        return coinsPickedUp ? 0 : coinValue;
    }

    /** Return the original amount of coins on this tile. */
    public int getOriginalCoinValue() {
        return coinValue;
    }
    
    /** Return the row of this Tile. */
    public int getRow() {
        return row;
    }
    
    /** Return the column of this Tile. */
    public int getColumn() {
        return col;
    }
    
    /**  Return the Type of this Tile.  */
    public Type getType() {
        return type;
    }
    
    /** Set the Type of this Tile to t. */
    /* package */ void setType(Type t){
        type = t;
    }
    
    /**  Set the value of coins on this Node to 0 and return the amount "taken" */
    public int takeCoins() {
        int result= coins();
        coinsPickedUp= true;
        return result;
    }
}
