public class SampleInvoke {

  public static int bar() {
    return 7;
  }

  public static int foo() {
    int i = 12;
    i = i + bar();
    return i;
  }

  public static int too() {
    return foo() + bar();
  }

  public static int two(int i, int k) {
    return i + k;
  }

  private static final String greeting = "Hello World!";

  public static void main(String[] args) {
    foo();
  }
}
