package game;

import java.util.Collection;

/** A GetOutState provides all the information necessary to
 * get out of the sewer system and collect coins on the way.
 * 
 * This interface provides access to the complete graph of the sewer system,
 * which will allow computation of the path.
 * Once you have determined how DiverMax should get out, call
 * moveTo(Node) repeatedly to move to each node. Coins on a node are picked up
 * automatically when that code is movedTo(...). */
public interface GetOutState {
    /** Return the Node corresponding to DiverMax's location in the graph. */
    public Node currentNode();

    /** Return the Node associated with the exit from the sewer system.
     * DiverMax has to move to this Node in order to get out. */
    public Node getExit();

    /** Return a collection containing all the nodes in the graph.
     * They in no particular order. */
    public Collection<Node> allNodes();

    /** Change DiverMax's location to n.
     * Throw an IllegalArgumentException if n is not directly connected to
     * DiverMax's location. */
    public void moveTo(Node n);

    /** Pick up the coins on the current tile. */
    public void grabCoins();

    /** Return the steps remaining to get out of the sewer system.
     * This value will change with every call to moveTo(Node),
     * and if it reaches 0 before you get out, you have failed to get out.  */
    public int stepsLeft();
}
