class InputData():
    '''

INPUT: 
    
    - time_series: set of time series. It is a list with length n (the number of time series)
                  Each time series has its own length
                  
    - PSTL template 
                  
    - par_bound : Parameter bounds for the PSTL template.
                  The list has length the number of parameters and 
                  to each parameter corresponds a pair of valuation boundaries.
                  
    - gran: grid granularity. The lenght is the number of parameters.
            Each element is a scalar representing the granularity in that parameter dimension. ''' 
            
# Possible kinds of approach : 
# - Binary satisfaction with fixed granularity
# - Binary satisfaction with binary search
# - Quantitative robustness with fixed granularity
# - Quantitative robustness with binary search




    def __init__(self, seed, traces, p_formula , par_bounds, granularity , sampling_freq):
        
        # seed : number representing the seed
        self.seed = seed
        
        
        # traces : list of the classes of (possibly multi-dimensional) traces
        #In particular, traces[0] is the list of time series in class 1, traces[1] class 2, ..
        self.traces = traces
        
        
        # p_formula: parametric STL formula in the form of a string
        # The numerical parameters to be mined have to be written as 'epsilon{numb}-', where {numb} is a positive integer number that identifies a particular parameter symbol
        # The syntax  to be used is the same as the monitor RTAMT: https://github.com/nickovic/rtamt
        # E.g. p_formula = 'always[10: epsilon0- ]( x > epsilon1- )', where epsilon0- and epsilon1- are the two parameters to be mined.
        self.p_formula = p_formula
        
        
        # par_bounds : list of the interval of admitted values for each parameter symbol appearing in p_formula
        # The order in the list has to follow the number in the parameter names, i.e. par_bounds[0] refers to epsilon0-
        # e.g., par_bounds = [ [1, 10], [-0.5, 11.2] ] indicates that epsilon0- varies in [1,10], while epsilon1- in [-0.5,11.2]
        self.par_bounds = par_bounds
        
        
        # granularity : list of the granularity values for each parameter. 
        # The order in the list has to follow the number in the parameter names, i.e. granularity[0] refers to epsilon0-
        # e.g., granularity = [1,2] indicates that the dimension of the cells that discretize the parameter space have length= 1 on the dimension of parameter epsilon0- and length = 2 on the dimension of parameter epsilon1-.
        # Granularity values have to follow the rule reported in the paper: there must exist a value k such that granularity[i] = (par_bounds[i][1]-par_bounds[i][0])/(2**k) for all i. 
        # In other words, the minimal cell resolution has to be reached by doing the same amount of splits in all parameter dimensions.
        self.granularity = granularity
        
        
        # samplig_freq: list of 3 elements to specify the frequency of the collection of the data points.
        # This is used to define spec.set_sampling_period( ) for RTAMT monitor.
        # In particular, spec.set_sampling_period(samplig_freq[0], samplig_freq,[1] samplig_freq[2] ), where:
        #    - samplig_freq[0] is the default expected period between two consecutive input samples 
        #    - samplig_freq[1] is a string representing the time units (e.g., 's' for seconds, 'ms' for milliseconds)
        #    - samplig_freq[2] is the percentage of error tolerance. 
        # E.g. samplig_freq = [ 1, 's', 0.1] means that data are collected every 1 second, but in the range of 0.9 and 1.1 are still accepted.
        # For more details, see https://github.com/nickovic/rtamt
        self.sampling_freq = sampling_freq
    
    
        # constant_definition : list of variables appearing in p_formula that the user wants to specify as constants (instead of variables) for the monitoring.
        # Each variable is specified as a list of two elements = [indx, type], where 
        #         - indx is the positive integer number representing the position of the variable in the traces.
        #           If, for example, each time series is made of = [time, variable x, variable y], then indx = 0 for variable time, indx =1 for variable x, and indx=2 for variable y. 
        #         - type is string indicating the type of the constant (e.g., 'float', 'int', 'bool')
        # The order of the variables in the list is not important.
        self.constant_definition = []
        
        
        # bool_mono : boolean variable to indicate whether to apply the monotonic variant (True) or not (False).
        # By default, it is set to False    
        self.bool_mono = False
        
        
        # mono : list of values to indicate the kind of monotonicity for each parameter. 
        # 1 represents increasing monotonicity, -1 decreasing.
        # The order in the list has to follow the number in the parameter names, i.e. mono[0] == 1 indicates that epsilon0- is a monotonic increasing parameter.
        # If bool_mono == False : this list is not even considered. 
        # By default, it is set to None
        self.mono = None 
        
        
        # bool_quantitative : boolean variable to indicate whether to apply the Quantitative approach (True) or not (False).
        # By default, it is set to False
        self.bool_quantitative = False  
        
        
        # bool_binary_search : boolean variable to indicate whether to apply the Binary Search approach (True) or not (False).
        # By default, it is set to False
        self.bool_binarysearch = False
        
        
        # bool_plot_figure : boolean variable to indicate whether to show the plots of the time series in the dataset and the validity domains (True) or not (False).
        # The validity domains are plotted only if they are 2 or 3 dimensional (i.e., with 2 or 3 parameters).
        # By default, it is set to False    
        self.bool_plot_figure = False
        
        # bool_store_results : boolean variable to indicate whether to store the approximation of the validity domains (True) or not (False).
        # By default, it is set to False    
        self.bool_store_results = False
        
        
        # percentage_training: number from 0 to 100 indicating the percentage of traces in the dataset 
        # that have to be used for the training phase (i.e. approximation of validity domains and choice of the parameter valuation)
        # The remainin ones are used for testing.
        # By default, it is set to None, this means that the user provides the exact number of traces to be used as training sample; the remaining ones are used for testing 
        self.percentage_training = None
        
        #if percentage_training = None       
        self.numb_train = None #number of traces to be used as training samples,  the remaining ones are used for testing 
        
        
        # bool_differente_templates : boolean variable to indicate whether two PSTL formulas should be used to characterize the two classes.
        # If bool_differente_templates == True, p_formula is associated with class 1 (traces[0]), while p_formula2 (to be defined) is used for class2 (traces[1]).
        # By default, it is set to False.    
        self.bool_different_templates = False
       
        
        # p_formula2 : parametric STL formula to be associated with the second class.
        # This variable is considered if and only if bool_differente_templates == True.
        # The rules are the same as for p_formula.
        self.p_formula2 = None
        
        
        ## The following variables refer to the specificties of the second parameteric formula p_formula2.
        ## Their explanation is analogous to the respective variables for the first formula p_formula.
        ## These variables are considered if and only if bool_differente_templates == True.
        
        self.par_bounds2 = None
        
        self.granularity2 = None
        
        self.sampling_freq2 = None
        
        self.constant_definition2 = []
        
        self.bool_mono2 = None
        
        self.mono2 = None 
        
        # bool_quantitative2 : boolean variable to indicate whether to apply the Quantitative approach (True) or not (False) when approximating the validity domains with respect to p_formula2.
        # bool_quantitative2 does not have to be the same as bool_quantitative
        # This varible is considered if and only if bool_differente_templates == True. For thir reason, it is set by default to None.
        self.bool_quantitative2 = None 
        
        # bool_binarysearch2 : boolean variable to indicate whether to apply the Binary Search approach (True) or not (False) when approximating the validity domains with respect to p_formula2.
        # bool_binarysearch2 does not have to be the same as bool_binarysearch
        # This varible is considered if and only if bool_differente_templates == True. For thir reason, it is set by default to None.
        self.bool_binarysearch2 = None
    
    
        self.file_name = 'text.text' # it is the file .txt where to write all the results
        
        
        self.bool_domain_knowledge = False #True if it exists domain knowledge for the choice of the parameters and the strategy  to search is implemented
        
        