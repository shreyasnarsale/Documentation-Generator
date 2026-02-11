package wordcountss;

import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.lang.InterruptedException;
import java.lang.ClassNotFoundException;

public class Driver{
	public static void main(String[] args) throws IOException ,InterruptedException, ClassNotFoundException {
		
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf,"wordcountss");
		
		job.setJarByClass(Driver.class);
		job.setMapperClass(My_Mapper.class);
		job.setReducerClass(My_Reducer.class);
		
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		job.waitForCompletion(true);
		
	}
}

