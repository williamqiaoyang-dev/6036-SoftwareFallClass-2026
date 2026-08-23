import java.util.ArrayList;
import java.util.Random;
import java.util.Stack;

public class Deck {
  public final Stack<Card> deck;

  public Deck(int cardCount) {
    cardCount = (int) (Math.ceil(cardCount / 4d) * 4);

    ArrayList<Card> temporaryDeck = new ArrayList<>();
    for (int i = 0; i < cardCount / 4; i++) {
      for (int j = 0; j < 4; j++) {
        temporaryDeck.add(new Card(j, i + 1));
      }
    }

    Random random = new Random();
    for (int i = 0; i < cardCount; i++) {
      int chosenIndex = random.nextInt(0, cardCount);
      int targetIndex = random.nextInt(0, cardCount);
      Card targetCard = temporaryDeck.get(targetIndex);

      temporaryDeck.set(targetIndex, temporaryDeck.get(chosenIndex));
      temporaryDeck.set(chosenIndex, targetCard);
    }

    deck = new Stack<>();
    deck.addAll(temporaryDeck);
  }

  public Deck(Stack<Card> cards) {
    deck = cards;
  }

  public Deck[] split() {
    Stack<Card> firstHalf = new Stack<>();
    Stack<Card> secondHalf = new Stack<>();

    firstHalf.addAll(deck.stream().limit(deck.size() / 2).toList());
    secondHalf.addAll(deck.stream().skip(deck.size() / 2).toList());
    return new Deck[] {new Deck(firstHalf), new Deck(secondHalf)};
  }
}
