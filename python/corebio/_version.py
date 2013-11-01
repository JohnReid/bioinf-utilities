

# Keywords between dollar signs are subsituted by subversion.
# The date and build will only tell the truth after a branch or tag,
# since different files in trunk will have been changed at different times
date ="$Date: 2006-11-27 12:10:21 -0800 (Mon, 27 Nov 2006) $".split()[1]
revision = "$Revision: 167 $".split()[1]

# major.minor.patch 
# The patch level should be zero in trunk, a positive number in a release 
# branch. During a release, increment the minor number in trunk and set the
# patch level to 1 in the branch. Increment patch number for bug fix releases.
__version__ = '0.5.0' #b' + revision 


description = "CoreBio %s (%s)" % (__version__,  date)


