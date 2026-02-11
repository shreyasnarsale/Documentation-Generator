package wordcountss;

import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

import java.io.IOException;

public class My_Reducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	
	public void reduce(Text word, Iterable<IntWritable> values,Context context) throws IOException, InterruptedException {
		int sum = 0;
		for (IntWritable value : values) {
			sum += value.get();
		}
		context.write(word, new IntWritable(sum));
	
	}
}
