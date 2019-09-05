package game;

import java.util.Collection;

/** The state of the game while performing looking for the ring..
 * In order to determine the next move, you need to call the various methods
 * of this interface. To move through the sewer system, you need to call moveTo(long).
 *
 * An instance provides all the information necessary
 * to search through the sewer system and find the ring.
 */
public interface FindState {
    /** Return the unique identifier associated with DiverMax's current location. */
    public long currentLocation();

    /** Return an unordered collection of NodeStatus objects
     * associated with all direct neighbors of DiverMax's current location.
     * Each status contains a unique identifier for the neighboring node
     * as well as the distance of that node to the ring along the grid<br><br>
     * (NB: This is NOT the distance in the graph, it is only the number
     *      of rows and columns away from the ring.)<br><br>
     * It is possible to move directly to any node identifier in this collection.
     */
    public Collection<NodeStatus> neighbors();

    /** Return DiverMax's current distance along the grid (NOT THE GRAPH) from
     * the ring. */
    public int distanceToRing();

    /** Change DiverMax's current location to the node given by id.<br><br>
     * Throw an IllegalArgumentException if the node with id id is not
     *    adjacent to DiverMax's current location. */
    public void moveTo(long id);
}
