package log;

import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import java.io.IOException;
import java.util.StringTokenizer;

public class My_Mapper extends Mapper<Object,Text, Text, IntWritable> {
	private final static IntWritable one = new IntWritable(1);
	private Text ipAddress = new Text();
	
	public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
		StringTokenizer itr = new StringTokenizer(value.toString(), " ");
				
				ipAddress.set(itr.nextToken());
				context.write(ipAddress,one);
				
	}
}