"""
Run this file at first, in order to see what it is printing.
Instead of the print() use the respective log level.
"""
############################### LOGGER
from abc import ABC, abstractmethod
from loguru import logger
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


#--------------------------------------#
class Bandit(ABC):
    """Abstract Base Class for Bandit algorithms."""
    ##==== DO NOT REMOVE ANYTHING FROM THIS CLASS ====##

    @abstractmethod
    def __init__(self, p):
        """
        p : list of true mean rewards for each bandit 
        """
        self.p = np.array(p)
        self.n_bandits = len(p)
        self.rewards = []
        self.chosen_bandits = []
        self.total_trials = 0
        self.algorithm_name = None  

    @abstractmethod
    def __repr__(self):
        """Representation string for debugging"""
        algo = self.algorithm_name if self.algorithm_name else "Unspecified Algorithm"
        return f"{algo} Bandit with {self.n_bandits} arms"

    @abstractmethod
    def pull(self, t):
        """Select a bandit to pull"""
        pass

    @abstractmethod
    def update(self, chosen_bandit, reward):
        """Update internal parameters"""
        pass

    @abstractmethod
    def experiment(self, n_trials=20000):
        """Run the bandit experiment"""
        logger.info(f"Starting experiment for {self.algorithm_name} with {n_trials} trials.")
        for t in range(n_trials):
            chosen_bandit = self.pull(t)
            reward = np.random.randn() + self.p[chosen_bandit]
            self.update(chosen_bandit, reward)
            self.rewards.append(reward)
            self.chosen_bandits.append(chosen_bandit)
        self.total_trials = n_trials
        logger.info(f"Finished experiment for {self.algorithm_name}.")

    @abstractmethod
    def report(self):
        """Store data in CSV and log average reward and regret."""
        df = pd.DataFrame({
            "Bandit": self.chosen_bandits,
            "Reward": self.rewards,
            "Algorithm": self.algorithm_name
        })

        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(base_dir, "data")
        os.makedirs(save_dir, exist_ok=True)

        csv_name = os.path.join(save_dir, f"{self.algorithm_name}_results.csv")
        df.to_csv(csv_name, index=False)
        logger.info(f"Results saved to {csv_name}")

        total_reward = np.sum(self.rewards)
        optimal_reward = np.max(self.p) * len(self.rewards)
        regret = optimal_reward - total_reward
        avg_reward = np.mean(self.rewards)
        avg_regret = regret / len(self.rewards)

        logger.info(f"=== {self.algorithm_name} Summary ===")
        logger.info(f"Total Trials: {self.total_trials}")
        logger.info(f"Average Reward: {avg_reward:.4f}")
        logger.info(f"Average Regret per Trial: {avg_regret:.4f}")
        logger.info(f"Total Regret: {regret:.2f}")
        logger.info(f"Optimal Bandit (True Mean): {np.argmax(self.p)}")


#--------------------------------------#
class Visualization:
    """Visualize performance of Epsilon-Greedy and Thompson Sampling."""
    
    def __init__(self, epsilon_greedy, thompson_sampling):
        self.eg = epsilon_greedy
        self.ts = thompson_sampling

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.vis_dir = os.path.join(base_dir, "img")
        os.makedirs(self.vis_dir, exist_ok=True)
    
    def plot1(self):
        """Visualize the performance of each bandit: linear and log"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Epsilon-Greedy Linear
        axes[0, 0].plot(np.cumsum(self.eg.rewards))
        axes[0, 0].set_title('Epsilon-Greedy: Cumulative Reward (Linear)')
        axes[0, 0].set_xlabel('Trials')
        axes[0, 0].set_ylabel('Cumulative Reward')
        axes[0, 0].grid(True)
        
        # Epsilon-Greedy Log
        axes[0, 1].plot(np.cumsum(self.eg.rewards))
        axes[0, 1].set_title('Epsilon-Greedy: Cumulative Reward (Log Scale)')
        axes[0, 1].set_xlabel('Trials')
        axes[0, 1].set_ylabel('Cumulative Reward')
        axes[0, 1].set_yscale('log')
        axes[0, 1].grid(True)
        
        # Thompson Sampling Linear
        axes[1, 0].plot(np.cumsum(self.ts.rewards))
        axes[1, 0].set_title('Thompson Sampling: Cumulative Reward (Linear)')
        axes[1, 0].set_xlabel('Trials')
        axes[1, 0].set_ylabel('Cumulative Reward')
        axes[1, 0].grid(True)
        
        # Thompson Sampling Log
        axes[1, 1].plot(np.cumsum(self.ts.rewards))
        axes[1, 1].set_title('Thompson Sampling: Cumulative Reward (Log Scale)')
        axes[1, 1].set_xlabel('Trials')
        axes[1, 1].set_ylabel('Cumulative Reward')
        axes[1, 1].set_yscale('log')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        save_path = os.path.join(self.vis_dir, 'rewards.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Plot 1 saved as {save_path}")
        plt.show()
    
    def plot2(self):
        """Compare E-greedy and Thompson sampling cumulative rewards and regrets"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Cumulative Rewards Comparison
        axes[0].plot(np.cumsum(self.eg.rewards), label='Epsilon-Greedy', alpha=0.8)
        axes[0].plot(np.cumsum(self.ts.rewards), label='Thompson Sampling', alpha=0.8)
        axes[0].set_title('Cumulative Rewards Comparison')
        axes[0].set_xlabel('Trials')
        axes[0].set_ylabel('Cumulative Reward')
        axes[0].legend()
        axes[0].grid(True)
        
        opt_reward = max(self.eg.p)
        eg_regret = opt_reward - np.array(self.eg.rewards)
        ts_regret = opt_reward - np.array(self.ts.rewards)
        
        # Cumulative Regrets Comparison
        axes[1].plot(np.cumsum(eg_regret), label='Epsilon-Greedy', alpha=0.8)
        axes[1].plot(np.cumsum(ts_regret), label='Thompson Sampling', alpha=0.8)
        axes[1].set_title('Cumulative Regrets Comparison')
        axes[1].set_xlabel('Trials')
        axes[1].set_ylabel('Cumulative Regret')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        save_path = os.path.join(self.vis_dir, 'algorithms_comparison.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Plot 2 saved as {save_path}")
        plt.show()


#--------------------------------------#
class EpsilonGreedy(Bandit):
    def __init__(self, p, epsilon=0.1):
        super().__init__(p)
        self.algorithm_name = "Epsilon-Greedy"
        self.epsilon = epsilon
        self.counts = np.zeros(self.n_bandits)
        self.values = np.zeros(self.n_bandits)

    def __repr__(self):
        return super().__repr__()

    def pull(self, t):
        eps_t = self.epsilon / (t + 1)
        if np.random.rand() < eps_t:
            return np.random.randint(self.n_bandits)
        return np.argmax(self.values)

    def update(self, chosen_bandit, reward):
        self.counts[chosen_bandit] += 1
        n = self.counts[chosen_bandit]
        value = self.values[chosen_bandit]
        self.values[chosen_bandit] = value + (1 / n) * (reward - value)

    def experiment(self, n_trials=20000):
        super().experiment(n_trials)

    def report(self):
        super().report()


#--------------------------------------#
class ThompsonSampling(Bandit):
    def __init__(self, p, tau=1.0):
        super().__init__(p)
        self.algorithm_name = "Thompson-Sampling"
        self.tau = tau
        self.m = np.zeros(self.n_bandits)
        self.lambda_ = np.ones(self.n_bandits)

    def __repr__(self):
        return super().__repr__()

    def pull(self, t):
        samples = np.random.randn(self.n_bandits) / np.sqrt(self.lambda_) + self.m
        return np.argmax(samples)

    def update(self, chosen_bandit, reward):
        self.m[chosen_bandit] = (
            self.tau * reward + self.lambda_[chosen_bandit] * self.m[chosen_bandit]
        ) / (self.tau + self.lambda_[chosen_bandit])
        self.lambda_[chosen_bandit] += self.tau

    def experiment(self, n_trials=20000):
        super().experiment(n_trials)

    def report(self):
        super().report()


#--------------------------------------#
def comparison(bandit_means, n_trials=20000):
    eps = EpsilonGreedy(bandit_means, epsilon=0.1)
    ts = ThompsonSampling(bandit_means, tau=1.0)

    eps.experiment(n_trials)
    ts.experiment(n_trials)

    eps.report()
    ts.report()

    vis = Visualization(eps, ts)
    vis.plot1()
    vis.plot2()


#--------------------------------------#
if __name__ == '__main__':
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    logger.info("Starting Experiment")

    Bandit_Reward = [1, 2, 3, 4]
    NumberOfTrials = 20000

    comparison(Bandit_Reward, n_trials=NumberOfTrials)
