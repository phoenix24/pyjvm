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

  public static int inc1(int a) {
    return a++;
  }

  public static int inc2(int a) {
    return ++a;
  }

  public static int neg(int a) {
    return -a;
  }

  public static int ifelse1() {
    if (1 > 0) {
      return 10;
    } else {
      return 15;
    }
  }

  public static boolean ifelse2() {
    return 2 > 3;
  }

  public static int ifeq(int a, int b) {
    return a == b ? a: b;
  }

  public static int ifgeq(int a, int b) {
    return a < b ? a: b;
  }

  public static int ifleq(int a, int b) {
    return a > b ? a: b;
  }

  public static int ifelse4() {
    return ifleq(4, 5);
  }

  public static int or(int a, int b) {
    return a | b;
  }

  public static int and(int a, int b) {
    return a & b;
  }

  public static int sub(int a, int b) {
    return a - b;
  }

  public static int mul(int a, int b) {
    return a * b;
  }

  public static int div(int a, int b) {
    return a / b;
  }

  public static int rem(int a, int b) {
    return a % b;
  }

  public static int calc1(int a, int b) {
    return (a  + b) * b;
  }

  public static String soo() {
    return "Hello";
  }

  public static String sood() {
    return "Hello" + " World!";
  }

  public static String hello() {
    return hello;
  }

  public static String hellow() {
    return hello + " " + world + "!";
  }

  private static final String hello = "Hello";
  private static final String world = "World";

  public static void main(String[] args) {
    foo();
  }
}
