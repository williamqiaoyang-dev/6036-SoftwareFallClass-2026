public class Card {
    public int suit;
    public int number;

    public Card(int suit, int number) {
        this.suit = suit;
        this.number = number;
    }

    @Override
    public String toString() {
        return String.format("%d of %s", number, switch (suit) {
          case 0 -> "Hearts";
          case 1 -> "Diamonds";
          case 2 -> "Clubs";
          case 3 -> "Spades";
          default -> "";
        });
    }
}
