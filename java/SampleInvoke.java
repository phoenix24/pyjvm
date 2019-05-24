public class SampleInvoke {

  public static int bar() {
    return 7;
  }

  public static int foo() {
    int i = 12;
    i = i + bar();
    return i;
  }

  private static final String greeting = "Hello World!";

  public static void main(String[] args) {
    foo();
  }
}
