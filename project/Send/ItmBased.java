
package ml_project;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.List;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.common.LongPrimitiveIterator;
import org.apache.mahout.cf.taste.impl.eval.RMSRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.recommender.CachingRecommender;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.UncenteredCosineSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.ItemSimilarity;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;



public class ItmBased {

    public ItmBased() {
        
        try
        {
            
            System.out.println("Item Based ");

                Object arr[][]=new Object[4][2];
               File ratingsFile = new File("C:/Users/Ankur/Desktop/ml-100k/u1.base");
            DataModel model = new FileDataModel(ratingsFile);

            
            RecommenderBuilder builder0 = new RecommenderBuilder() {
                
                public Recommender buildRecommender(DataModel model) throws TasteException {
                   
                   ItemSimilarity itemSimilarity = new PearsonCorrelationSimilarity(model);   
                  
                    return new CachingRecommender(new GenericItemBasedRecommender(model, itemSimilarity));
                }
            };
            RecommenderEvaluator evaluator0 = new RMSRecommenderEvaluator();
            double score0 = evaluator0.evaluate(builder0, null,model,0.8,0.2);
            System.out.println("With PearsonCorrelation= " + score0);
             arr[1][0]=new String("PearsonCorrelation");arr[1][1]=new Double(score0);

            
             
                RecommenderBuilder builder1 = new RecommenderBuilder() {
                
                public Recommender buildRecommender(DataModel model) throws TasteException {
                   
                   ItemSimilarity itemSimilarity = new EuclideanDistanceSimilarity(model);   
                  
                    return new CachingRecommender(new GenericItemBasedRecommender(model, itemSimilarity));
                }
            };
            RecommenderEvaluator evaluator1 = new RMSRecommenderEvaluator();
            double score1 = evaluator1.evaluate(builder1, null,model,0.8,0.2);
            System.out.println("With EuclideanDistance= " + score1);
            arr[2][0]=new String("EuclideanDistance");arr[2][1]=new Double(score1);
             
             
             
             
             RecommenderBuilder builder2 = new RecommenderBuilder() {
                
                public Recommender buildRecommender(DataModel model) throws TasteException {
                   
                   ItemSimilarity itemSimilarity = new UncenteredCosineSimilarity(model);   
                  
                    return new CachingRecommender(new GenericItemBasedRecommender(model, itemSimilarity));
                }
            };
            RecommenderEvaluator evaluator2 = new RMSRecommenderEvaluator();
            double score2 = evaluator1.evaluate(builder2, null,model,0.8,0.2);
            System.out.println("With CosineDistance= " + score2);
            arr[3][0]=new String("CosineDistance");arr[3][1]=new Double(score1);
             
             CreateImage(arr);

        }
        catch(Exception e)
        {
            System.out.print(e);
        }
    }

    
    
    void CreateImage(Object arr[][])
    {
         try {
                
                /* Step - 1: Define the data for the line chart  */
                DefaultCategoryDataset line_chart_dataset = new DefaultCategoryDataset();

                for(int i=1;i<arr.length;i++)
                {
                   //System.out.print("ANkur");
                        line_chart_dataset.addValue(Double.parseDouble(arr[i][1].toString()), "Classifier", arr[i][0].toString());
                    
                }
                
                /* Step -2:Define the JFreeChart object to create line chart */
                JFreeChart lineChartObject=ChartFactory.createLineChart("Classifier vs Error","Classifier","RMS Error",line_chart_dataset,PlotOrientation.VERTICAL,true,true,true);                
                          
                /* Step -3 : Write line chart to a file */               
                 int width=640; /* Width of the image */
                 int height=480; /* Height of the image */                
                 File lineChart=new File("C:/Users/Ankur/Desktop/ItemBased.png");              
                 ChartUtilities.saveChartAsPNG(lineChart,lineChartObject,width,height); 
         }
         catch (Exception i)
         {
             System.out.println(i);
         }
    }

    
    
    void meanSquare(Recommender recommend) {
        try {

            File ratingsFile = new File("C:/Users/Ankur/Desktop/ml-100k/u1.test");
            BufferedReader buff = new BufferedReader(new FileReader(ratingsFile));
            //DataModel model = new FileDataModel(ratingsFile);

            float mean = 0;
            float value = 0;
            float count =0;
            String line = null;
            String[] temp;
            while ((line = buff.readLine()) != null) {
                count++;

                temp = line.split("\t");
                System.out.println(temp[0] + "  " + temp[1] + "  " + temp[2]);
                value = recommend.estimatePreference(Integer.parseInt(temp[0]), Integer.parseInt(temp[1]));
               // value = Math.round(value);
                System.out.println("Value   " + value);
                mean += Math.pow((value - Double.parseDouble(temp[2])), 2);
            }

            double ans=mean/count;
             System.out.println("Mean Squre Error ="+ ans);

            


        } catch (Exception e) {

            
        System.out.println(e);
        }

    }
    
    public static void main(String [] args)
    {
        new ItmBased();
    }
}
