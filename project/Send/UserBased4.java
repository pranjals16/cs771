package ml_project;

import javax.swing.*;

import org.math.plot.*;
import java.io.File;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.RMSRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.CachingRecommender;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.EuclideanDistanceSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.UncenteredCosineSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;
import org.apache.mahout.common.distance.CosineDistanceMeasure;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

public class UserBased4 {

    public UserBased4() {


        try {
           
            System.out.println("With User Based ");
           Object rms_neighbour[][]=new Object[900][2];int j=1;
            for(int i=2;i<=102;i=i+10)
            {
                rms_neighbour[j][0]=new Integer(i);
                rms_neighbour[j][1]=new Double(get_rms_score(i));
                System.out.println("At "+i+" Users = "+get_rms_score(i));
                j++;
                
            }
           
      //    CreateImage(rms_neighbour);

        } catch (Exception e) {
            System.out.println(e);
        }
    }

    double get_rms_score(final int i)
    {
        try{
             File ratingsFile = new File("C:/Users/Ankur/Desktop/ml-100k/ua.base");
             DataModel model = new FileDataModel(ratingsFile);
           
              RecommenderBuilder builder = new RecommenderBuilder() {
                public Recommender buildRecommender(DataModel model) throws TasteException {
                    // UserSimilarity userSimilarity = new PearsonCorrelationSimilarity(model);
                   // UserSimilarity userSimilarity = new EuclideanDistanceSimilarity(model);
                    UserSimilarity userSimilarity = new UncenteredCosineSimilarity(model);
                       UserNeighborhood neighborhood =
                    new NearestNUserNeighborhood(i, userSimilarity, model);
                    return new CachingRecommender(new GenericUserBasedRecommender(model, neighborhood, userSimilarity));
                }
            };
            RecommenderEvaluator evaluator = new RMSRecommenderEvaluator();
            double score = evaluator.evaluate(builder, null,model,0.8,0.2);
            
            return score;
    }
        catch(Exception e)
        {
            System.out.println(e);
        }
        return 1;
    }
    
      
    void CreateImage(Object arr[][])
    {
         try {
                
                /* Step - 1: Define the data for the line chart  */
                DefaultCategoryDataset line_chart_dataset = new DefaultCategoryDataset();

                for(int i=1;i<=11;i++)
                {
                   //System.out.print("ANkur");
                        line_chart_dataset.addValue(Double.parseDouble(arr[i][1].toString()), "Error_Rate", arr[i][0].toString());
                    
                }
                
                /* Step -2:Define the JFreeChart object to create line chart */
                JFreeChart lineChartObject=ChartFactory.createLineChart("CosineSimilarity","Number_of_users","RMS Error",line_chart_dataset,PlotOrientation.VERTICAL,true,true,true);                
                          
                /* Step -3 : Write line chart to a file */               
                 int width=640; /* Width of the image */
                 int height=480; /* Height of the image */                
                 File lineChart=new File("C:/Users/Ankur/Desktop/User_based_CosineCoeffiecintSimila.png");              
                 ChartUtilities.saveChartAsPNG(lineChart,lineChartObject,width,height); 
         }
         catch (Exception i)
         {
             System.out.println(i);
         }
    }
    
    
    public static void main(String[] args) {
        new UserBased4();
    }
}
