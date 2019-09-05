package student;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

import game.GetOutState;
import game.Tile;
import game.FindState;
import game.SewerDiver;
import game.Node;
import game.NodeStatus;
import game.Edge;

public class DiverMax extends SewerDiver {


    /** Get to the ring in as few steps as possible. Once you get there, 
     * you must return from this function in order to pick
     * it up. If you continue to move after finding the ring rather 
     * than returning, it will not count.
     * If you return from this function while not standing on top of the ring, 
     * it will count as a failure.
     * 
     * There is no limit to how many steps you can take, but you will receive
     * a score bonus multiplier for finding the ring in fewer steps.
     * 
     * At every step, you know only your current tile's ID and the ID of all 
     * open neighbor tiles, as well as the distance to the ring at each of these tiles
     * (ignoring walls and obstacles). 
     * 
     * In order to get information about the current state, use functions
     * currentLocation(), neighbors(), and distanceToRing() in FindState.
     * You know you are standing on the ring when distanceToRing() is 0.
     * 
     * Use function moveTo(long id) in FindState to move to a neighboring 
     * tile by its ID. Doing this will change state to reflect your new position.
     * 
     * A suggested first implementation that will always find the ring, but likely won't
     * receive a large bonus multiplier, is a depth-first walk. Some
     * modification is necessary to make the search better, in general.*/
    @Override public void findRing(FindState state) {
        //TODO : Find the ring and return.
        // DO NOT WRITE ALL THE CODE HERE. DO NOT MAKE THIS METHOD RECURSIVE.
        // Instead, write your method elsewhere, with a good specification,
        // and call it from this one.
        
    	HashSet<Long>visited = new HashSet<Long>();
    	helpFindRing(state, visited);
    	
    	
    }
    
    
    /** Helper function for findRing(FindState).
     * This method originated with the dfs-walk algorithm. It is optimized using 
     * each location's manhattan distance from the ring. It'll choose the direction 
     * based on the shortest distance from the ring. This is done using a min-heap. 
     * This heap keeps track of where the neighboring locations are. 
     * 
     * Also, only the neighbors not already visited will be visited. If a dead end
     * is hit, this method will bring the person back to its original location before
     * it recursed, and will continue to move to locations not already visited.
     * 
     */
    public void helpFindRing(FindState state, HashSet<Long> visited) {
    	if(state.distanceToRing() == 0) return; //Found the ring
    	
    	long current = state.currentLocation();
    	visited.add(current);
    	
    	//holds all the neighbors in a min-heap
    	Heap<NodeStatus>neighbors = new Heap<NodeStatus>(); 
    	
    	for(NodeStatus neighbor:state.neighbors()) {
    		if(!visited.contains(neighbor.getId())) //minimize space
    			neighbors.add(neighbor, neighbor.getDistanceToTarget());
    	}
    	int size = neighbors.size();
    	for(int i = 0; i < size; i++) {
    		NodeStatus neighbor = neighbors.poll();
    		if(!visited.contains(neighbor.getId())) { //reduce time walking
    			state.moveTo(neighbor.getId());
    			helpFindRing(state, visited);
    			if(state.distanceToRing() == 0) return;
    			state.moveTo(current);
    		}
    	}
    }
    
    
    /** Get out of the sewer system before the steps are all used, trying to collect
     * as many coins as possible along the way. Your solution must ALWAYS get out
     * before the steps are all used, and this should be prioritized above
     * collecting coins.
     * 
     * You now have access to the entire underlying graph, which can be accessed
     * through GetOutState. currentNode() and getExit() will return Node objects
     * of interest, and getNodes() will return a collection of all nodes on the graph. 
     * 
     * You have to get out of the sewer system in the number of steps given by
     * getStepsRemaining(); for each move along an edge, this number is decremented
     * by the weight of the edge taken.
     * 
     * Use moveTo(n) to move to a node n that is adjacent to the current node.
     * When n is moved-to, coins on node n are automatically picked up.
     * 
     * You must return from this function while standing at the exit. Failing to
     * do so before steps run out or returning from the wrong node will be
     * considered a failed run.
     * 
     * Initially, there are enough steps to get from the starting point to the
     * exit using the shortest path, although this will not collect many coins.
     * For this reason, a good starting solution is to use the shortest path to
     * the exit. */
    @Override public void getOut(GetOutState state) {
        //TODO: Get out of the sewer system before the steps are used up.
        // DO NOT WRITE ALL THE CODE HERE. Instead, write your method elsewhere,
        //with a good specification, and call it from this one.
    	
    	//Iterates through all the nodes and adds the coins to an arraylist to keep
    	//track of how many coins are left on the map.
    	Collection <Node> n = state.allNodes();
    	Iterator itr = n.iterator();
    	List <Node> allcoins = new ArrayList <Node>();
    	while(itr.hasNext()) {
    		Node node = (Node) itr.next();
    		if(node.getTile().coins() > 0)
    			allcoins.add(node);
    	}
    	
    	helpGetOut(state, allcoins);
    }
    
    
    /** Helper function that takes in the state and the list of all coins available
     * on the map prior moving or collecting. The list of nodes can be empty, and 
     * this is handled in the shortest path algorithm in Paths.shortestPath(). 
     * 
     * Uses closestCoin() helper function to find the next closest coin as Max 
     * traverses through the map. 
     * 
     * Max will pick up any coins on his current tile, then he looks for the next
     * closest coin using the helper function. If there's more coins, but not enough
     * steps, Max will begin going towards the exit. However, while going towards 
     * the exit, if Max finds a coin close by that's reachable (still able to leave
     * within the remaining steps), he'll go collect those coins and finally continue. 
     * This patterns continues until he makes it to the exit. 
     * 
     * Furthermore, if there's no close enough coins at all, Max will not calculate 
     * further as he'll head directly towards the exit (picking up any coins on the 
     * path).  */
    public void helpGetOut(GetOutState state, List<Node> nodes) {
    	//Create the node coin before the loops begin. This is the variable that 
    	//continues and ends the loop.
    	Node coin = null; 
    	do { //do-while loop b/c we want to iterate one time first no matter what
    		coin = closestCoin(state, nodes);
        	List <Node> coinExitPath = Paths.shortestPath(coin, state.getExit());
        	List <Node> pathToCoin = Paths.shortestPath(state.currentNode(), coin);
        	int distTocoinToExit = Paths.pathDistance(coinExitPath) + 
        								Paths.pathDistance(pathToCoin);
        	
        	/* Makes sure the coin isn't too far away, if it is, choose another close
        	* coin to collect. If all coins are too far, coin = null.  	*/
        	while(distTocoinToExit > state.stepsLeft() && coin != null) {
        		if(nodes.size()==0) 
        			coin = null; //ends both while loops
        		else {
	        		nodes.remove(coin);
        			if(nodes.size()!=0) {
	        			coin = closestCoin(state, nodes);
		        		coinExitPath = Paths.shortestPath(coin, state.getExit());
		            	pathToCoin = Paths.shortestPath(state.currentNode(), coin);
		            	distTocoinToExit = Paths.pathDistance(coinExitPath) + 
		            						Paths.pathDistance(pathToCoin);
        			}
        		}
        	} //end while
        	
        	if(state.currentNode() == coin) //picks up coin when standing on it
        		state.grabCoins();
        	else if(coin!=null) { //go to the coin that's closest (not null)
		        for(int i = 1; i < pathToCoin.size(); i++) 
		        	state.moveTo(pathToCoin.get(i));
    		}
        	
    		if(coin != null) //helps while loops towards termination
    			nodes.remove(coin);
    		if(nodes.size() == 0) //code above may remove the last coin
    			coin = null; //ends loop if no more coins able to be collected
    		
    	}while(coin!=null);
    	
    	//Time to leave, takes the shortest path to exit
    	List <Node> path = Paths.shortestPath(state.currentNode(), state.getExit());
        for(int i = 1; i < path.size(); i++) 
        	state.moveTo(path.get(i));
        
    } //end of helpGetOut
    
    
    /** Private helper function for helpGetOut().
     * 
     *  This is private, because only helpGetOut() requires this method. 
     *  As Max traverses through the map, we'll need to calculate the next closest
     *  coin to Max. This is the function to do that. 
     *  
     *  This function takes in state and the list of nodes (not all the nodes prior
     *  to moving/collecting). This method looks through all the nodes given and
     *  picks out the closest node to Max using the shortest path algorithm. */
    private Node closestCoin(GetOutState state, List<Node> nodes) {
    	Node closestcoin = null;
    	int dist = Integer.MAX_VALUE;
    	for(Node node:nodes) {
			int path = Paths.pathDistance(Paths.shortestPath(state.currentNode(), node));
			if(path < dist) {
				dist = path;
				closestcoin = node;
			}
    	}
    	return closestcoin; //null if no coins closest
    }
    
}
