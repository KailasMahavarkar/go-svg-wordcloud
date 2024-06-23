class Solution:
    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        self.result = set()

        def dfs(i, arr):

            if i >= len(nums):
                if len(arr) >= 2:
                    self.result.add(tuple(arr))
                return

            if len(arr) >= 2:
                self.result.add(tuple(arr))

            # Pick
            if (not arr) or (arr[-1] <= nums[i]):
                # print(i, arr)
                dfs(i + 1, arr + [nums[i]])

            # Unpick
            dfs(i + 1, arr)
            return
        dfs(0, [])
        return list(self.result)
