public class SampleInvoke1 {

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

  public static int taa() {
    return bar() + foo();
  }

  public static int tee() {
    return bar() + bar();
  }

  public static int two(int i, int k) {
    return i + k;
  }

  public static int twod() {
    return two(1, 3);
  }

  public static String stwod() {
    return greeting;
  }

  private static final String greeting = "Hello World!";

  public static void main(String[] args) {
    foo();
  }
}
