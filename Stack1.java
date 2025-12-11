import java.util.Stack;
public class Stack1{
    public static void pushAtBottom(Stack<Integer>s,int data){
        if(s.isEmpty()){
            s.push(data);
            return;
        }
        int top=s.pop();
        pushAtBottom(s,data);
        s.push(top);
    }
    public static String reverseString(String str){
        Stack<Character>s=new Stack<>();
        int idx=0;
        while(idx<str.length()){
            s.push(str.charAt(idx));
            idx++;
        }
        StringBuilder result=new StringBuilder("");
        while(!s.isEmpty()){
            result.append(s.pop());
        }
        return result.toString();
    }
    public static void printStack(Stack<Integer>s){
        while(!s.isEmpty()){
            System.out.println(s.pop());
        }
    }
    public static void reverseStack(Stack<Integer>s){
        if(s.isEmpty()){
            return;
        }
        int top=s.pop();
        reverseStack(s);
        pushAtBottom(s,top);
    }
    public static void stockSpan(int stock[]){
        Stack<Integer>s=new Stack<>();
        int span[]=new int [stock.length];
        span[0]=1;
        s.push(0);
        for(int i=1;i<stock.length;i++){
            int currPrice=stock[i];
            while(!s.isEmpty() && currPrice>stock[s.peek()]){
                s.pop();
            }
            if(s.isEmpty()){
                span[i]=i+1;
            }else{
                int prevHigh=s.peek();
                span[i]=i-prevHigh;
            }
            s.push(i);
        }
        for(int i=0;i<span.length;i++){
            System.out.print(span[i]+" ");
        }
    }
    public static void findNextGreater(int arr[]){
        Stack<Integer>s=new Stack<>();
        int nextGreater[]=new int[arr.length];
        for(int i=arr.length-1;i>=0;i--){
            while(!s.isEmpty() && arr[s.peek()]<=arr[i]){
                s.pop();
            }
            if(s.isEmpty())nextGreater[i]=-1;
            else{
                nextGreater[i]=arr[s.peek()];
            }
            s.push(i);
        }
        for(int i=0;i<nextGreater.length;i++){
            System.out.print(nextGreater[i]+" ");
        }
    }
    public static boolean isValidParentheses(String str){
        Stack<Character> s=new Stack<>();
        for(int i=0;i<str.length();i++){
            Character ch=str.charAt(i);
            if(ch=='('||ch=='{'||ch=='['){// opening
                s.push(ch);
            }else{
                if(s.isEmpty())return false;
                Character ch1=s.peek();
                if((ch1=='(' && ch==')')||(ch1=='{' && ch=='}')||(ch1=='[' && ch==']')){
                    s.pop();
                }else return false;
            }
        }
        if(s.isEmpty())return true;
        else return false;
    }
    public static boolean isDuplicate(String str){
        Stack<Character>s=new Stack<>();
        for(int i=0;i<str.length();i++){
            char ch=str.charAt(i);
            if(ch==')'){
                int count=0;
                while(s.peek()!='('){
                    s.pop();
                    count++;
                }
                if(count<1)return true;
                else s.pop();
            }else{
                s.push(ch);
            }
        }
        return false;
    }
    public static void maxAreaInHistogram(int arr[]){
        int []nsr=new int[arr.length];
        int []nsl=new int[arr.length];
        int maxArea=0;
        //Next Smaller Right
        Stack<Integer>s=new Stack<>();
        for(int i=arr.length-1;i>=0;i--){
            while(!s.isEmpty() && arr[s.peek()]>=arr[i]){
                s.pop();
            }
            if(s.isEmpty()){
                nsr[i]=arr.length;
            }else{
                nsr[i]=s.peek();
            }
            s.push(i);
        }
        // Next Smaller Left
        s=new Stack<>();
        for(int i=0;i<arr.length;i++){
            while(!s.isEmpty() && arr[s.peek()]>=arr[i]){
                s.pop();
            }
            if(s.isEmpty()){
                nsl[i]=arr.length;
            }else{
                nsl[i]=s.peek();
            }
            s.push(i);
        }
        // current Area
        for(int i=0;i<arr.length;i++){
         int height=arr[i];
         int width=nsr[i]-nsl[i]-1;
         int current=height*width;
         maxArea=Math.max(current,maxArea);
        }
        System.out.println("ARR\tNSR\tNSL");
        for(int i=0;i<arr.length;i++){
            System.out.println(arr[i]+"\t"+nsr[i]+"\t"+nsl[i]);
        }
        System.out.println("Maximum area of histogram is ="+maxArea);
    }
    public static void main(String args[]){
        String str="[({}[]())]";
        String str1="(a+b)";
        String str2="((a+b))";
        int arr[]={2,1,5,6,1,3};
        Stack<Integer> s=new Stack<>();
        s.push(2);
        s.push(3);
        s.push(4);
        s.push(5);
        pushAtBottom(s,1);
        System.out.println(reverseString(str));
        reverseStack(s);
        System.out.println("----Reverse Stack----");
        printStack(s);
        int stock[]={100,80,60,70,60,85,100};
        stockSpan(stock);
        findNextGreater(arr);
        System.out.println(isValidParentheses(str));
        System.out.println(isDuplicate(str2));
        maxAreaInHistogram(arr);
    }
}