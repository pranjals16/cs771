package netflix.algorithms.modelbased;

public abstract class AbstractModelBuilder {
    /**
     * Builds a model, and writes to database
     * @return true if model was completely built
     */
    protected abstract boolean buildModel();
    
    protected abstract boolean buildModel(String outputFile);
}
