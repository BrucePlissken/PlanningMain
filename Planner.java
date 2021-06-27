import JSHOP2.*;
import java.io.*;
import JSHOP2.Calculate;

class Planner implements Calculate {
    InternalDomain idomain;
    File file;
    //JSHOP2Parser parser;
    Planner(){
        file = new File("tmp/basic/basic");
        // parser = new JSHOP2Parser();
        start();
        
    }
    
    public Term call(List l){


        return l.getHead();
    }

    public void start(){
        String path = "tmp/basic/basic";
        String path2 = "tmp/basic/problem";
        String[] stringArray = new String[1];
        stringArray[0] = path;
        String[] stringArrayTwo = new String[2];
        stringArrayTwo[0] = "-ra";
        stringArrayTwo[1] = path2;
        try {
            idomain = new InternalDomain(file, 2);
            idomain.main(stringArray);
            idomain.main(stringArrayTwo);

            
        } catch (Exception e) {
            //TODO: handle exception
            System.out.println("exception " + e);
        }
    }        
        
       
        
        
        
    public static void main(String[] args) {
        
        new Planner();
    }
}