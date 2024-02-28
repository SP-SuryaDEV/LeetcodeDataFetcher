import backoff
import requests

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=10)
def returnQuery(username, name, regno, year, dept, section, domain, mail, phone):
    url = 'https://leetcode.com/graphql'


    headers = {
        'Content-Type': 'application/json',
    }

    # Define your GraphQL query
    query = '''
        query combinedQueries($username: String!) {
            matchedUser(username: $username) {
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
            userContestRanking(username: $username) {
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
                topPercentage
                badge {
                    name
                }
            }
        }
    '''

    variables = {
        "username": f"{username}"
    }

    payload = {
        'query': query,
        'variables': variables
    }

    response = requests.post(url, json=payload, headers=headers)

    

    if response.status_code == 200:
        json_dict = response.json()

        if not json_dict:
            return None

        matchedUser = json_dict['data']['matchedUser']

        contestCount,rating,globalRank,topPercent = 0,0,0,0
        easy, medium, hard, total = 0, 0, 0, 0

        if  matchedUser:
            problems_solved = matchedUser['submitStatsGlobal']['acSubmissionNum']

            for pair in problems_solved:
                if pair['difficulty'] == 'All':
                    total = pair['count']
                elif pair['difficulty'] == 'Easy':
                    easy = pair['count']
                elif pair['difficulty'] == 'Medium':
                    medium = pair['count']
                elif pair['difficulty'] == 'Hard':
                    hard = pair['count']

            score = easy + medium * 2 + hard * 3

        else:
            return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username, 'Mail ID' : mail, 'Mobile Number' : phone}, False


        contest = json_dict['data']['userContestRanking']

        if  contest:

            for key, value in contest.items():
                if key == 'attendedContestsCount':
                    contestCount = value
                elif key == 'rating':
                    rating = value
                elif key == 'globalRanking':
                    globalRank = value
                elif key == 'topPercentage':
                    topPercent = value

        return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username,'Easy' : easy, 'Medium' : medium, 'Hard' : hard, 'Total' : total, 'Score' : score,'Total Contests Count' : contestCount, 'Contest Rating' : rating, 'Global Rank' : globalRank, 'Top%' : topPercent, 'Mail ID' : mail, 'Mobile Number' : phone}, True


    else:
        print(f"Failed to fetch data for user: {username}")
        return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username, 'Mail ID' : mail, 'Mobile Number' : phone}, False
        
    
