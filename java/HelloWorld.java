public class HelloWorld {
    
    private final static String greeting = "Hello World!";
    
    public int add(int a, int b) {
	return a + b;
    }

    public int multiply(int a) {
	return a * 5;
    }


    public static void main(String[] args) {
	HelloWorld hw = new HelloWorld();
	int result1 = hw.add(100, 50);
	int result2 = hw.multiply(result1);
	System.out.println("Hello World! " + result2);
    }
}