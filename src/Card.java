public class Card {
    public int suit;
    public int number;

    public Card(int suit, int number) {
        this.suit = suit;
        this.number = number;
    }

    @Override
    public String toString() {
        return String.format("Suit: %d, Number: %d", suit, number);

    }
}
