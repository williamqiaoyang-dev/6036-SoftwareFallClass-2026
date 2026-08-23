import java.util.ArrayList;

public class Main {
  public static void main(String[] args) {
    Deck[] decks = new Deck(52).split();
    Deck player1 = decks[0];
    Deck player2 = decks[1];

    ArrayList<Card> pool = new ArrayList<>();

    while (true) {
      Card card1 = player1.deck.pop();
      Card card2 = player2.deck.pop();

      if (card1.number < card2.number) {
        System.out.printf("Player 2's card %s was greater than Player 1's card %s\n", card2, card1);
        player2.deck.addLast(card1);
        player2.deck.addLast(card2);
        if (!pool.isEmpty()) {
          System.out.println("Player 2 also won " + pool + ".");
          player2.deck.addAll(pool);
          pool.clear();
        }
      } else if (card1.number > card2.number) {
        System.out.printf("Player 1's card %s was greater than Player 2's card %s\n", card1, card2);
        player1.deck.addLast(card1);
        player1.deck.addLast(card2);
        if (!pool.isEmpty()) {
          System.out.println("Player 1 also won " + pool + ".");
          player1.deck.addAll(pool);
          pool.clear();
        }
      } else {
        System.out.printf("WAR with Player 1's card %s and Player 2's card %s\n", card1, card2);
        pool.add(card1);
        pool.add(card2);
      }

      if (player1.deck.isEmpty() && player2.deck.isEmpty()) {
        System.out.println("\nIt's a tie!");
        break;
      } else if (player1.deck.isEmpty()) {
        System.out.println("\nPlayer 1 won!");
        break;
      } else if (player2.deck.isEmpty()) {
        System.out.println("\nPlayer 2 won!");
        break;
      }

      System.out.println("=========================");
    }
  }
}
