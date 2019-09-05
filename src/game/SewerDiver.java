package game;

/** An abstract class representing what methods a sewer diver
 *  must implement in order to be used in solving the game.*/
public abstract class SewerDiver {
	
	 /** 
     * Explore the sewer, trying to find the 
     * ring in as few steps as possible. Once you find the 
     * ring, return from findRing in order to pick
     * it up. If you continue to move after finding the ring rather 
     * than returning, it will not count.
     * If you return from this function while not standing on top of the ring, 
     * it will count as a failure.
     * 
     * There is no limit to how many steps you can take, but you will receive
     * a score bonus multiplier for finding the ring in fewer steps.
     * 
     * At every step, you only know your current tile's ID and the ID of all 
     * open neighbor tiles, as well as the distance to the ring at each of these tiles
     * (ignoring walls and obstacles). 
     * 
     * In order to get information about the current state, use functions
     * getCurrentLocation(), getNeighbors(), and getDistanceToTarget() in FindState.
     * You know you are standing on the ring when getDistanceToTarget() is 0.
     * 
     * Use function moveTo(long id) in FindState to move to a neighboring 
     * tile by its ID. Doing this will change state to reflect your new position.
     * 
     * A suggested first implementation that will always find the find, but likely
     * won't receive a large bonus multiplier, is a depth-first walk.
     * 
     * @param state the information available at the current state
     */
    public abstract void findRing(FindState state);

    /** Get out of the sewer in within a certain number of steps, trying to collect
     * as many coins as possible along the way. Your solution must ALWAYS get out
     * before using up all the steps, and this should be prioritized above collecting
     * coins.
     * 
     * You now have access to the entire underlying graph, which can be accessed
     * through GetOutState. currentNode() and getExit() return Node objects of
     * interest, and getNodes() returns a collection of all nodes on the graph. 
     * 
     * Look at interface GetOutState.
     * You can find out how many steps are left for DiverMax to take using function
     * stepsLeft. Each time DiverMax traverses an edge, the steps left are
     * decremented by the weight of that edge. You can use grabCoins() to pick up any
     * coins on your current tile (this will fail if no coins are there), and
     * moveTo() to move to a destination node adjacent to your current node.
     * 
     * You must return from this function while standing at the exit. Failing to do so
     * within the steps left or returning from the wrong location will be considered a
     * failed run.
     * 
     * You will always have enough time to get out using the shortest path from the
     * starting position to the exit, although this will not collect many coins. But
     * for this reason, using Dijkstra's to plot the shortest path to the exit is
     * a good starting solution.
     * 
     * @param state the information available at the current state */
    public abstract void getOut(GetOutState state);
}
