import JSHOP2.*;
import java.io.*;

class Planner {
    InternalDomain idomain;
    File file;
    JSHOP2Parser parser;

    public static void main(String[] args) {
        
        new Planner();
    }
    
    Planner(){
        file = new File("tmp/basic/basic");
        parser = new JSHOP2Parser();
        start();

    }
    
    public void start(){
        
        //System.out.print( );
       
        try {
            idomain = new InternalDomain(file, 2);
            idomain.parser.command();
            
        } catch (Exception e) {
            //TODO: handle exception
            System.out.println("exception " + e);
        }

        


    }
}