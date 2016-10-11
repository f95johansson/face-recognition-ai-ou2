import java.io.File;
import java.io.IOException;
import java.util.Scanner;

public class FaceTest2 {
    static Scanner resultFile = null;
    static Scanner facitFile = null;

    public FaceTest2() {
    }

    public static void main(String[] var0) {
        if(var0.length != 1) {
            System.out.println("Usage: java FaceTest");
            System.exit(-1);
        }

        try {
            resultFile = new Scanner(new File(var0[0]));
            facitFile = new Scanner(System.in);
        } catch (IOException var5) {
            var5.printStackTrace();
        }

        int var1 = 0;
        int var2 = 0;

        int var3;
        do {
            var3 = loadFacit(resultFile);
            if(var3 > 0) {
                int var4 = loadFacit(facitFile);
                if(var3 == var4) {
                    ++var1;
                }

                ++var2;
            }
        } while(var3 > 0);

        System.out.print("Percentage of correct classifications: " + 100.0D * (double)var1 / (double)var2);
        System.out.println("% out of " + var2 + " images");
    }

    private static int loadFacit(Scanner var0) {
        if(!var0.hasNext()) {
            return -1;
        } else {
            String var1;
            do {
                var1 = var0.next();
            } while(var0.hasNext() && !var1.startsWith("Image"));

            int var2 = -1;
            if(var0.hasNextInt()) {
                var2 = var0.nextInt();
            }

            return var2;
        }
    }
}
