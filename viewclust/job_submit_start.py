from datetime import datetime
import numpy as np
import pandas as pd

def job_submit_start(jobs):

	end=jobs['submit'] + (jobs['end'] - jobs['start'])
	jobs['start']=jobs['submit']
	jobs['end']=end

	return jobs


